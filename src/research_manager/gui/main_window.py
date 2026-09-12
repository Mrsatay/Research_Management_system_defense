from __future__ import annotations

from html import escape
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSplitter,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from ..config import get_settings
from ..models import Paper
from ..services.paper_service import PaperService, PaperValidationError
from .paper_dialog import PaperDialog

TABLE_HEADERS = [
    "Paper ID",
    "Title",
    "Authors",
    "Institution",
    "Publication",
    "Publication Date",
    "Keywords",
    "Abstract",
]


class MainWindow(QMainWindow):
    def __init__(self, paper_service: PaperService, parent=None) -> None:
        super().__init__(parent)
        self.paper_service = paper_service
        self.current_papers: list[Paper] = []
        self.sort_descending = True
        self.setWindowTitle("Research Paper Information Management System")
        self.resize(1280, 760)
        self._build_menu()
        self._build_ui()
        self.refresh_table()

    def _build_menu(self) -> None:
        file_menu = self.menuBar().addMenu("&File")
        add_action = QAction("Add Paper", self)
        add_action.setShortcut("Ctrl+N")
        add_action.triggered.connect(self.add_paper)
        file_menu.addAction(add_action)
        import_action = QAction("Import CSV", self)
        import_action.triggered.connect(self.import_csv)
        file_menu.addAction(import_action)
        export_action = QAction("Export CSV", self)
        export_action.triggered.connect(self.export_csv)
        file_menu.addAction(export_action)
        file_menu.addSeparator()
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        manage_menu = self.menuBar().addMenu("&Manage")
        edit_action = QAction("Edit Selected Paper", self)
        edit_action.setShortcut("Ctrl+E")
        edit_action.triggered.connect(self.edit_paper)
        manage_menu.addAction(edit_action)
        delete_action = QAction("Delete Selected Papers", self)
        delete_action.setShortcut("Delete")
        delete_action.triggered.connect(self.delete_papers)
        manage_menu.addAction(delete_action)

        view_menu = self.menuBar().addMenu("&View")
        refresh_action = QAction("Refresh", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self.refresh_table)
        view_menu.addAction(refresh_action)
        sort_action = QAction("Toggle Date Sort", self)
        sort_action.triggered.connect(self.toggle_sort)
        view_menu.addAction(sort_action)
        stats_action = QAction("Publication Statistics", self)
        stats_action.triggered.connect(self.show_statistics)
        view_menu.addAction(stats_action)

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(22, 20, 22, 20)
        root.setSpacing(14)

        heading = QHBoxLayout()
        title = QLabel("Research Paper Library")
        title.setObjectName("pageTitle")
        heading.addWidget(title)
        heading.addStretch()
        self.total_label = QLabel("0 papers")
        self.total_label.setObjectName("statValue")
        heading.addWidget(self.total_label)
        root.addLayout(heading)

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by title or author...")
        self.search_input.setMinimumWidth(300)
        self.search_input.textChanged.connect(self.refresh_table)
        toolbar.addWidget(self.search_input)
        refresh_button = QPushButton("Refresh")
        refresh_button.setObjectName("secondaryButton")
        refresh_button.clicked.connect(self.refresh_table)
        toolbar.addWidget(refresh_button)
        sort_button = QPushButton("Sort by Date")
        sort_button.setObjectName("secondaryButton")
        sort_button.clicked.connect(self.toggle_sort)
        toolbar.addWidget(sort_button)
        root.addWidget(toolbar)

        action_bar = QHBoxLayout()
        for text, callback, object_name in (
            ("Add Paper", self.add_paper, ""),
            ("Edit Selected", self.edit_paper, "secondaryButton"),
            ("Delete Selected", self.delete_papers, "dangerButton"),
            ("Publication Statistics", self.show_statistics, "secondaryButton"),
        ):
            button = QPushButton(text)
            if object_name:
                button.setObjectName(object_name)
            button.clicked.connect(callback)
            action_bar.addWidget(button)
        action_bar.addStretch()
        root.addLayout(action_bar)

        splitter = QSplitter(Qt.Vertical)
        self.table = QTableWidget(0, len(TABLE_HEADERS))
        self.table.setHorizontalHeaderLabels(TABLE_HEADERS)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.ExtendedSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.doubleClicked.connect(self.edit_paper)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setColumnWidth(0, 110)
        self.table.setColumnWidth(1, 270)
        self.table.setColumnWidth(2, 210)
        self.table.setColumnWidth(3, 180)
        self.table.setColumnWidth(4, 180)
        self.table.setColumnWidth(5, 125)
        self.table.setColumnWidth(6, 220)
        self.table.setColumnWidth(7, 320)
        splitter.addWidget(self.table)

        self.abstract_preview = QLabel("Select a paper to preview its abstract.")
        self.abstract_preview.setWordWrap(True)
        self.abstract_preview.setMinimumHeight(75)
        self.abstract_preview.setStyleSheet(
            "background: #ffffff; border: 1px solid #d9e0eb; padding: 12px;"
        )
        self.table.itemSelectionChanged.connect(self.update_preview)
        splitter.addWidget(self.abstract_preview)
        splitter.setSizes([570, 120])
        root.addWidget(splitter, 1)
        self.setStatusBar(QStatusBar())

    def refresh_table(self) -> None:
        self.current_papers = self.paper_service.list_papers(
            self.search_input.text(), self.sort_descending
        )
        self.table.setRowCount(len(self.current_papers))
        for row, paper in enumerate(self.current_papers):
            values = [
                paper.paper_id,
                paper.title,
                paper.authors,
                paper.institution,
                paper.publication,
                paper.publication_date.isoformat(),
                paper.keywords,
                paper.abstract[:180] + ("..." if len(paper.abstract) > 180 else ""),
            ]
            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setData(Qt.UserRole, paper.id)
                self.table.setItem(row, column, item)
        self.total_label.setText(f"{len(self.current_papers)} papers")
        direction = "newest first" if self.sort_descending else "oldest first"
        self.statusBar().showMessage(f"Showing {len(self.current_papers)} paper(s), {direction}.")
        self.update_preview()

    def selected_papers(self) -> list[Paper]:
        rows = sorted({index.row() for index in self.table.selectedIndexes()})
        return [self.current_papers[row] for row in rows if row < len(self.current_papers)]

    def add_paper(self) -> None:
        dialog = PaperDialog(self.paper_service, parent=self)
        if dialog.exec():
            self.refresh_table()

    def edit_paper(self) -> None:
        papers = self.selected_papers()
        if len(papers) != 1:
            QMessageBox.information(self, "Select one paper", "Select exactly one paper to edit.")
            return
        dialog = PaperDialog(self.paper_service, papers[0], parent=self)
        if dialog.exec():
            self.refresh_table()

    def delete_papers(self) -> None:
        papers = self.selected_papers()
        if not papers:
            QMessageBox.information(self, "No selection", "Select one or more papers to delete.")
            return
        answer = QMessageBox.question(
            self,
            "Confirm deletion",
            f"Delete {len(papers)} selected paper(s)? This cannot be undone.",
        )
        if answer == QMessageBox.Yes:
            self.paper_service.delete_papers(paper.id for paper in papers)
            self.refresh_table()

    def toggle_sort(self) -> None:
        self.sort_descending = not self.sort_descending
        self.refresh_table()

    def update_preview(self) -> None:
        papers = self.selected_papers()
        if not papers:
            self.abstract_preview.setText("Select a paper to preview its abstract.")
            return
        paper = papers[0]
        self.abstract_preview.setText(
            f"<b>{escape(paper.title)}</b><br>{escape(paper.abstract)}"
        )

    def show_statistics(self) -> None:
        counts = self.paper_service.count_by_publication()
        if not counts:
            message = "No paper records are available."
        else:
            message = "\n".join(f"{publication}: {count}" for publication, count in counts)
        QMessageBox.information(self, "Publication Statistics", message)

    def import_csv(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Paper Text File",
            str(get_settings().export_directory),
            "CSV/Text files (*.csv *.txt)",
        )
        if not path:
            return
        try:
            imported, errors = self.paper_service.import_csv(path)
        except PaperValidationError as exc:
            QMessageBox.warning(self, "Import failed", str(exc))
            return
        self.refresh_table()
        message = f"Imported {imported} paper(s)."
        if errors:
            message += "\n\nSkipped rows:\n" + "\n".join(errors[:10])
            if len(errors) > 10:
                message += f"\n... and {len(errors) - 10} more."
            QMessageBox.warning(self, "Import completed with warnings", message)
        else:
            QMessageBox.information(self, "Import completed", message)

    def export_csv(self) -> None:
        default_path = Path(get_settings().export_directory) / "papers_export.csv"
        path, _ = QFileDialog.getSaveFileName(
            self, "Export Paper Text File", str(default_path), "CSV/Text files (*.csv *.txt)"
        )
        if not path:
            return
        count = self.paper_service.export_csv(path)
        QMessageBox.information(self, "Export completed", f"Exported {count} paper(s).")
