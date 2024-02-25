# Imports
from pathlib import Path
from views.disk_view import FileNav
from views.analyzer_view import Analyzer
from viewmodels.mediator import Mediator
# Qt
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QSplitter
)


class Window(QMainWindow):
    """Main app GUI window."""

    ### Constants ###
    WIDTH = 1200  #pixels
    HEIGHT = 700  #pixels

    def __init__(self):
        super().__init__(parent = None)
        self._build()

    def _build(self):
        # Window properties
        icon_path = Path(__file__).parents[1] / 'data/logo.ico'
        self.setWindowIcon(QIcon(str(icon_path)))
        self.setWindowTitle("Power Analyzer")
        self.resize(Window.WIDTH, Window.HEIGHT)

        # Custom widgets
        filenav = FileNav()
        analyzer = Analyzer()

        # Compose mediator for widget view-models (data highway)
        Mediator(filenav.viewmodel, analyzer.viewmodel)

        # Put file navigation in its own pane
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(filenav)
        splitter.addWidget(analyzer)

        # Compose remaining view features
        layout = QHBoxLayout()
        layout.addWidget(splitter)

        # Establish core layout
        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)