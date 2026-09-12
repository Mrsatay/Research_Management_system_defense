from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication, QMessageBox

from ..database import initialize_database
from ..services.auth_service import AuthService
from ..services.paper_service import PaperService
from .login_window import LoginWindow
from .main_window import MainWindow
from .styles import APP_STYLESHEET


def run_application() -> None:
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLESHEET)
    try:
        initialize_database()
        auth_service = AuthService()
        auth_service.ensure_default_admin()
    except Exception as exc:
        QMessageBox.critical(
            None,
            "Database connection error",
            "Could not connect to PostgreSQL.\n\n"
            "Check that PostgreSQL is running and your .env settings are correct.\n\n"
            f"Technical detail: {exc}",
        )
        return

    login = LoginWindow(auth_service)
    if login.exec() != LoginWindow.Accepted:
        return
    window = MainWindow(PaperService())
    window.show()
    sys.exit(app.exec())
