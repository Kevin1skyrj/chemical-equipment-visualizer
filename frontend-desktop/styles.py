"""Centralized style sheet for the PyQt dashboard."""

DASHBOARD_QSS = """
QMainWindow {
    background-color: #eef2ff;
}

QFrame#HeroCard {
    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #eff6ff, stop:1 #ffffff);
    border: 1px solid #d9e3ff;
    border-radius: 20px;
}

QFrame#Card {
    background-color: #ffffff;
    border: 1px solid #dfe4f6;
    border-radius: 16px;
}

QLabel#HeroEyebrow {
    color: #2563eb;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.3em;
    text-transform: uppercase;
}

QLabel#HeroTitle {
    color: #0f172a;
    font-size: 22px;
    font-weight: 700;
}

QLabel#HeroSubtitle {
    color: #475569;
    font-size: 13px;
}

QLabel#HeroMeta {
    color: #1d4ed8;
    font-size: 12px;
    font-weight: 600;
}

QLabel#SectionTitle {
    color: #0f172a;
    font-size: 15px;
    font-weight: 600;
}

QLabel#SectionSubtitle {
    color: #64748b;
    font-size: 12px;
}

QPushButton {
    background-color: #2563eb;
    color: #ffffff;
    border-radius: 10px;
    padding: 8px 18px;
    font-weight: 600;
    border: none;
}

QPushButton:hover {
    background-color: #1d4ed8;
}

QPushButton:pressed {
    background-color: #1e3a8a;
}

QPushButton:disabled {
    background-color: #9db8ff;
    color: #e2e8f0;
}

QPushButton[variant="ghost"] {
    background-color: #eff6ff;
    color: #1d4ed8;
    border: 1px solid #bfdbfe;
}

QLineEdit, QListWidget, QTextEdit {
    border: 1px solid #cbd5f5;
    border-radius: 10px;
    padding: 6px 10px;
    background-color: #ffffff;
}

QLineEdit:read-only {
    background-color: #f8fafc;
}

QTableWidget {
    border: 1px solid #cbd5f5;
    border-radius: 12px;
    gridline-color: #e2e8f0;
    alternate-background-color: #f8fafc;
}

QHeaderView::section {
    background-color: #eef2ff;
    border: none;
    border-bottom: 1px solid #dfe4f6;
    padding: 6px;
    font-weight: 600;
    color: #475569;
}

QListWidget {
    padding: 8px;
}

QListWidget::item {
    border-radius: 8px;
    padding: 8px;
    margin: 4px 0;
}

QListWidget::item:selected {
    background-color: #dbeafe;
    color: #1d4ed8;
}
"""
