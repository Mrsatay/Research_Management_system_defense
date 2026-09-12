from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from ..services.auth_service import AuthService


class LoginWindow(QDialog):
    authenticated = Signal()

    def __init__(self, auth_service: AuthService, parent=None) -> None:
        super().__init__(parent)
        self.auth_service = auth_service
        self.setWindowTitle("Research Paper Manager - Login")
        self.setFixedSize(420, 300)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(38, 32, 38, 32)
        title = QLabel("Research Paper Manager")
        title.setObjectName("pageTitle")
        title.setAlignment(Qt.AlignCenter)
        subtitle = QLabel("Sign in to manage your research library")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addWidget(subtitle)

        form = QFormLayout()
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        form.addRow("Username", self.username_input)
        form.addRow("Password", self.password_input)
        layout.addLayout(form)

        login_button = QPushButton("Log In")
        login_button.clicked.connect(self._login)
        self.password_input.returnPressed.connect(self._login)
        layout.addWidget(login_button)
        layout.addStretch()
        hint = QLabel("Default demo account: admin / admin123")
        hint.setAlignment(Qt.AlignCenter)
        hint.setStyleSheet("color: #64748b;")
        layout.addWidget(hint)

    def _login(self) -> None:
        if self.auth_service.authenticate(
            self.username_input.text(), self.password_input.text()
        ):
            self.authenticated.emit()
            self.accept()
        else:
            QMessageBox.warning(
                self,
                "Login failed",
                "The username or password is incorrect.",
            )
