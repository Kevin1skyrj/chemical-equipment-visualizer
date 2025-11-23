"""Centralized style sheet for the PyQt dashboard."""

DASHBOARD_QSS = """
* {
    font-family: 'Segoe UI', 'SF Pro Display', 'Arial', sans-serif;
}

QMainWindow {
    background-color: #f1f5f9;
}

QFrame#HeroCard {
    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #dbeafe, stop:1 #ffffff);
    border: 2px solid #bfdbfe;
    border-radius: 16px;
    padding: 20px;
}

QFrame#Card {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 16px;
}

QLabel#HeroEyebrow {
    color: #2563eb;
    font-size: 10px;
    font-weight: 700;
}

QLabel#HeroTitle {
    color: #1e293b;
    font-size: 24px;
    font-weight: 700;
}

QLabel#HeroSubtitle {
    color: #475569;
    font-size: 14px;
}

QLabel#HeroMeta {
    color: #3b82f6;
    font-size: 11px;
    font-weight: 600;
}

QLabel#SectionTitle {
    color: #1e293b;
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 4px;
}

QLabel#SectionSubtitle {
    color: #64748b;
    font-size: 13px;
    margin-bottom: 8px;
}

QLabel {
    color: #334155;
    font-size: 13px;
}

QPushButton {
    background-color: #2563eb;
    color: #ffffff;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 600;
    font-size: 13px;
    border: none;
    min-height: 36px;
}

QPushButton:hover {
    background-color: #1e40af;
}

QPushButton:pressed {
    background-color: #1e40af;
}

QPushButton:disabled {
    background-color: #cbd5e1;
    color: #94a3b8;
}

QPushButton[variant="ghost"] {
    background-color: #f1f5f9;
    color: #2563eb;
    border: 1px solid #cbd5e1;
}

QPushButton[variant="ghost"]:hover {
    background-color: #e0e7ff;
    border-color: #a5b4fc;
}

QLineEdit, QListWidget, QTextEdit {
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 8px 12px;
    background-color: #ffffff;
    font-size: 13px;
    color: #1e293b;
    selection-background-color: #dbeafe;
}

QLineEdit:focus, QListWidget:focus {
    border: 2px solid #3b82f6;
}

QLineEdit:read-only {
    background-color: #f1f5f9;
    color: #64748b;
}

QTableWidget {
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    gridline-color: #e2e8f0;
    alternate-background-color: #f8fafc;
    background-color: #ffffff;
    font-size: 13px;
    color: #334155;
}

QTableWidget::item {
    padding: 8px;
}

QTableWidget::item:selected {
    background-color: #dbeafe;
    color: #1e293b;
}

QHeaderView::section {
    background-color: #f1f5f9;
    border: none;
    border-bottom: 2px solid #cbd5e1;
    padding: 10px 8px;
    font-weight: 700;
    font-size: 12px;
    color: #64748b;
    text-transform: uppercase;
}

QListWidget {
    padding: 4px;
}

QListWidget::item {
    border-radius: 6px;
    padding: 12px;
    margin: 2px 4px;
    border: 1px solid transparent;
}

QListWidget::item:hover {
    background-color: #f1f5f9;
    border-color: #cbd5e1;
}

QListWidget::item:selected {
    background-color: #eff6ff;
    border-color: #93c5fd;
    color: #1e40af;
    font-weight: 600;
}

QScrollArea {
    border: none;
    background-color: #f1f5f9;
}

QScrollBar:vertical {
    background-color: #f1f5f9;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #cbd5e1;
    border-radius: 6px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #94a3b8;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}
"""
