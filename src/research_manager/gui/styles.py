APP_STYLESHEET = """
QMainWindow, QDialog {
    background: #f5f7fb;
    color: #172033;
}
QMenuBar {
    background: #172033;
    color: #ffffff;
    padding: 5px;
}
QMenuBar::item:selected, QMenu::item:selected {
    background: #2d6cdf;
}
QMenu {
    background: #ffffff;
    color: #172033;
    border: 1px solid #d9e0eb;
}
QToolBar {
    background: #ffffff;
    border: none;
    spacing: 8px;
    padding: 8px;
}
QLabel#pageTitle {
    color: #172033;
    font-size: 22px;
    font-weight: 700;
}
QLabel#statValue {
    color: #2d6cdf;
    font-size: 22px;
    font-weight: 700;
}
QLineEdit, QTextEdit, QDateEdit, QTableWidget, QComboBox {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    padding: 7px;
}
QLineEdit:focus, QTextEdit:focus, QDateEdit:focus, QComboBox:focus {
    border: 2px solid #2d6cdf;
}
QPushButton {
    background: #2d6cdf;
    color: #ffffff;
    border: none;
    border-radius: 4px;
    padding: 8px 14px;
    font-weight: 600;
}
QPushButton:hover {
    background: #1f56b8;
}
QPushButton#secondaryButton {
    background: #e7edf7;
    color: #172033;
}
QPushButton#dangerButton {
    background: #cf3d4f;
}
QTableWidget {
    gridline-color: #e1e7f0;
    selection-background-color: #dce9ff;
    selection-color: #172033;
}
QHeaderView::section {
    background: #e7edf7;
    color: #172033;
    padding: 8px;
    border: none;
    font-weight: 700;
}
QGroupBox {
    background: #ffffff;
    border: 1px solid #d9e0eb;
    border-radius: 6px;
    margin-top: 12px;
    padding: 14px;
    font-weight: 700;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 5px;
}
"""
