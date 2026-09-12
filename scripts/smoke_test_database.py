from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from research_manager.database import initialize_database
from research_manager.services.auth_service import AuthService
from research_manager.services.paper_service import PaperService


def main() -> None:
    initialize_database()
    AuthService().ensure_default_admin()
    service = PaperService()
    existing = service.get_by_id("SMOKE-001")
    if existing is not None:
        service.delete_papers([existing.id])

    paper = service.add_paper(
        {
            "paper_id": "SMOKE-001",
            "title": "Smoke Test Paper for Defense Verification",
            "authors": "Codex Tester",
            "institution": "Research Management Lab",
            "publication": "Defense Verification Journal",
            "publication_date": "2024-06-01",
            "abstract": "Temporary record used to verify database operations.",
            "keywords": "smoke test; verification",
        }
    )
    assert service.get_by_id("SMOKE-001") is not None
    assert service.list_papers("Defense Verification", descending=False)
    assert service.count_by_publication()
    service.update_paper(
        paper.id,
        {
            "paper_id": "SMOKE-001",
            "title": "Updated Smoke Test Paper for Defense Verification",
            "authors": "Codex Tester",
            "institution": "Research Management Lab",
            "publication": "Defense Verification Journal",
            "publication_date": "2024-06-02",
            "abstract": "Temporary updated record used to verify database operations.",
            "keywords": "smoke test; verification; update",
        },
    )
    export_path = Path("data") / "smoke_export.csv"
    count = service.export_csv(export_path)
    assert export_path.exists()
    service.delete_papers([paper.id])
    print(f"Database smoke test passed. Exported {count} record(s) during verification.")


if __name__ == "__main__":
    main()
