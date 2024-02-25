# Imports
# Qt
from PySide6.QtCore import Qt, QDir
from PySide6.QtWidgets import QFileSystemModel


class DiskModel(QFileSystemModel):
    """Represents filesystem with a directory-only filter applied."""

    def __init__(self):
        super().__init__()
        self.setFilter(
            QDir.Filter.NoDotAndDotDot |
            QDir.Filter.AllDirs
        )

    #TODO: Add @override for Python >=3.12
    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ):
        """Overrides headerData for custom column 0 label."""

        if ((section == 0) and (role == Qt.ItemDataRole.DisplayRole)):
            return "Directory"
        else:
            return super().headerData(section, orientation, role)