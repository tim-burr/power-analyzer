# Imports
from viewmodels.disk_vm import DiskViewModel
# Qt
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QLineEdit, QListView, QTreeView,
    QVBoxLayout, QSplitter
)


class UrlBox(QLineEdit):
    """Accepts absolute path to target directory."""

    def __init__(self):
        super().__init__()
        self._build()

    def _build(self):
        self.setPlaceholderText("Enter test directory path...")
        self.setObjectName("url")  # Enable styling by name

class DirTree(QTreeView):
    """Tree view of available directories."""

    def __init__(self):
        super().__init__()

    def format(self):
        """Hides all tree view columns except for the first."""

        for i in range(1, 4):
            self.hideColumn(i)


class FileList(QListView):
    """List of compatible files for analysis."""

    def __init__(self):
        super().__init__()


class FileNav(QWidget):
    """Combined directory and file navigation pane.

    Attributes:
        viewmodel: A DiskViewModel object, which is the view's assigned model.
    """

    def __init__(self):
        super().__init__()
        self.viewmodel: DiskViewModel
        self._build()

    def _build(self):
        # Define views
        url_box = UrlBox()
        dir_tree = DirTree()
        file_list = FileList()

        # Define view-model
        self.viewmodel = DiskViewModel(
            url_box, dir_tree, file_list
        )

        # Define layout
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(dir_tree)
        splitter.addWidget(file_list)

        layout = QVBoxLayout()
        layout.addWidget(url_box)
        layout.addWidget(splitter)
        self.setLayout(layout)