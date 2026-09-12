from __future__ import annotations

from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QTextEdit,
    QVBoxLayout,
)

from ..models import Paper
from ..services.paper_service import PaperService, PaperValidationError


class PaperDialog(QDialog):
    def __init__(
        self,
        paper_service: PaperService,
        paper: Paper | None = None,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self.paper_service = paper_service
        self.paper = paper
        self.setWindowTitle("Edit Paper" if paper else "Add Paper")
        self.setMinimumSize(650, 560)
        self._build_ui()
        if paper:
            self._load_paper(paper)

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        form = QFormLayout()
        form.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)

        self.paper_id_input = QLineEdit()
        self.title_input = QLineEdit()
        self.authors_input = QLineEdit()
        self.institution_input = QLineEdit()
        self.publication_input = QLineEdit()
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setMaximumDate(QDate.currentDate())
        self.abstract_input = QTextEdit()
        self.abstract_input.setMinimumHeight(120)
        self.keywords_input = QLineEdit()

        form.addRow("Paper ID *", self.paper_id_input)
        form.addRow("Paper Title *", self.title_input)
        form.addRow("Authors *", self.authors_input)
        form.addRow("Institution *", self.institution_input)
        form.addRow("Publication *", self.publication_input)
        form.addRow("Publication Date *", self.date_input)
        form.addRow("Abstract *", self.abstract_input)
        form.addRow("Keywords *", self.keywords_input)
        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self._save)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _load_paper(self, paper: Paper) -> None:
        self.paper_id_input.setText(paper.paper_id)
        self.title_input.setText(paper.title)
        self.authors_input.setText(paper.authors)
        self.institution_input.setText(paper.institution)
        self.publication_input.setText(paper.publication)
        self.date_input.setDate(
            QDate(
                paper.publication_date.year,
                paper.publication_date.month,
                paper.publication_date.day,
            )
        )
        self.abstract_input.setPlainText(paper.abstract)
        self.keywords_input.setText(paper.keywords)

    def form_data(self) -> dict:
        return {
            "paper_id": self.paper_id_input.text(),
            "title": self.title_input.text(),
            "authors": self.authors_input.text(),
            "institution": self.institution_input.text(),
            "publication": self.publication_input.text(),
            "publication_date": self.date_input.date().toString("yyyy-MM-dd"),
            "abstract": self.abstract_input.toPlainText(),
            "keywords": self.keywords_input.text(),
        }

    def _save(self) -> None:
        try:
            if self.paper:
                self.paper_service.update_paper(self.paper.id, self.form_data())
            else:
                self.paper_service.add_paper(self.form_data())
        except (PaperValidationError, ValueError) as exc:
            QMessageBox.warning(self, "Validation error", str(exc))
            return
        self.accept()
