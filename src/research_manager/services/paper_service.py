from __future__ import annotations

import csv
from datetime import date, datetime
from pathlib import Path
from typing import Iterable

from sqlalchemy import delete, func, or_, select
from sqlalchemy.exc import IntegrityError

from ..database import session_scope
from ..models import Paper

PAPER_FIELDS = (
    "paper_id",
    "title",
    "authors",
    "institution",
    "publication",
    "publication_date",
    "abstract",
    "keywords",
)


class PaperValidationError(ValueError):
    """Raised when a paper record does not satisfy input rules."""


class DuplicatePaperError(ValueError):
    """Raised when a paper ID already exists."""


class PaperService:
    """Business logic for paper records and file operations."""

    @staticmethod
    def validate(data: dict) -> dict:
        cleaned = {
            key: "" if data.get(key) is None else str(data.get(key, "")).strip()
            for key in PAPER_FIELDS
        }
        required_text = (
            "paper_id",
            "title",
            "authors",
            "institution",
            "publication",
            "abstract",
            "keywords",
        )
        missing = [field for field in required_text if not cleaned[field]]
        if missing:
            raise PaperValidationError(
                f"Required fields are missing: {', '.join(missing)}."
            )
        try:
            parsed_date = datetime.strptime(
                cleaned["publication_date"], "%Y-%m-%d"
            ).date()
        except ValueError as exc:
            raise PaperValidationError(
                "Publication date must use the format YYYY-MM-DD."
            ) from exc
        if parsed_date > date.today():
            raise PaperValidationError("Publication date cannot be in the future.")
        cleaned["publication_date"] = parsed_date
        return cleaned

    def list_papers(self, search_text: str = "", descending: bool = True) -> list[Paper]:
        with session_scope() as session:
            statement = select(Paper)
            search_text = search_text.strip()
            if search_text:
                pattern = f"%{search_text}%"
                statement = statement.where(
                    or_(Paper.title.ilike(pattern), Paper.authors.ilike(pattern))
                )
            order_column = (
                Paper.publication_date.desc()
                if descending
                else Paper.publication_date.asc()
            )
            statement = statement.order_by(order_column, Paper.paper_id.asc())
            return list(session.scalars(statement).all())

    def get_by_id(self, paper_id: str) -> Paper | None:
        with session_scope() as session:
            return session.scalar(select(Paper).where(Paper.paper_id == paper_id))

    def add_paper(self, data: dict) -> Paper:
        cleaned = self.validate(data)
        with session_scope() as session:
            paper = Paper(**cleaned)
            session.add(paper)
            try:
                session.flush()
            except IntegrityError as exc:
                raise DuplicatePaperError(
                    f"Paper ID '{cleaned['paper_id']}' already exists."
                ) from exc
            session.refresh(paper)
            return paper

    def update_paper(self, record_id: int, data: dict) -> Paper:
        cleaned = self.validate(data)
        with session_scope() as session:
            paper = session.get(Paper, record_id)
            if paper is None:
                raise PaperValidationError("The selected paper no longer exists.")
            for key, value in cleaned.items():
                setattr(paper, key, value)
            try:
                session.flush()
            except IntegrityError as exc:
                raise DuplicatePaperError(
                    f"Paper ID '{cleaned['paper_id']}' already exists."
                ) from exc
            session.refresh(paper)
            return paper

    def delete_papers(self, record_ids: Iterable[int]) -> int:
        ids = list(record_ids)
        if not ids:
            return 0
        with session_scope() as session:
            result = session.execute(delete(Paper).where(Paper.id.in_(ids)))
            return result.rowcount or 0

    def count_by_publication(self) -> list[tuple[str, int]]:
        with session_scope() as session:
            statement = (
                select(Paper.publication, func.count(Paper.id))
                .group_by(Paper.publication)
                .order_by(func.count(Paper.id).desc(), Paper.publication.asc())
            )
            return [(publication, count) for publication, count in session.execute(statement)]

    def import_csv(self, file_path: str | Path) -> tuple[int, list[str]]:
        imported = 0
        errors: list[str] = []
        with Path(file_path).open("r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)
            missing_headers = [
                field
                for field in PAPER_FIELDS
                if field not in (reader.fieldnames or [])
            ]
            if missing_headers:
                raise PaperValidationError(
                    f"CSV is missing columns: {', '.join(missing_headers)}."
                )
            for row_number, row in enumerate(reader, start=2):
                try:
                    self.add_paper(row)
                    imported += 1
                except (PaperValidationError, DuplicatePaperError) as exc:
                    errors.append(f"Row {row_number}: {exc}")
        return imported, errors

    def export_csv(self, file_path: str | Path) -> int:
        papers = self.list_papers(search_text="", descending=False)
        with Path(file_path).open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=PAPER_FIELDS)
            writer.writeheader()
            for paper in papers:
                writer.writerow(
                    {
                        "paper_id": paper.paper_id,
                        "title": paper.title,
                        "authors": paper.authors,
                        "institution": paper.institution,
                        "publication": paper.publication,
                        "publication_date": paper.publication_date.isoformat(),
                        "abstract": paper.abstract,
                        "keywords": paper.keywords,
                    }
                )
        return len(papers)
