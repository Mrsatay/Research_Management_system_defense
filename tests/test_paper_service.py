from datetime import date, timedelta

import pytest

from research_manager.services.paper_service import PaperService, PaperValidationError


def valid_record() -> dict:
    return {
        "paper_id": "P-100",
        "title": "A Valid Research Paper",
        "authors": "Test Author",
        "institution": "Test Institution",
        "publication": "Test Journal",
        "publication_date": "2024-01-15",
        "abstract": "A sufficiently descriptive abstract.",
        "keywords": "testing; research",
    }


def test_validate_converts_date_to_date_object():
    result = PaperService.validate(valid_record())
    assert result["publication_date"] == date(2024, 1, 15)


def test_validate_rejects_missing_required_field():
    record = valid_record()
    record["title"] = ""
    with pytest.raises(PaperValidationError):
        PaperService.validate(record)


def test_validate_rejects_future_date():
    record = valid_record()
    record["publication_date"] = (date.today() + timedelta(days=1)).isoformat()
    with pytest.raises(PaperValidationError):
        PaperService.validate(record)
