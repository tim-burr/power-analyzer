# Imports
from pathlib import Path
# Qt
from PySide6.QtWidgets import QApplication


class Style:
    """Loads and applies externally-defined QSS styles to application."""

    def __init__(self, app: QApplication):
        with open(Path(__file__).parents[1] / 'data/style.qss', 'r') as f:
            app.setStyleSheet(f.read())