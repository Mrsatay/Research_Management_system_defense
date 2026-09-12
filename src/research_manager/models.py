from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Date, DateTime, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )


class Paper(Base):
    __tablename__ = "papers"
    __table_args__ = (
        UniqueConstraint("paper_id", name="uq_papers_paper_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    paper_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    authors: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    institution: Mapped[str] = mapped_column(String(300), nullable=False)
    publication: Mapped[str] = mapped_column(String(300), nullable=False, index=True)
    publication_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    abstract: Mapped[str] = mapped_column(Text, nullable=False)
    keywords: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
