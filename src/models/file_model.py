# Imports
from pathlib import Path
from utilities.data_loader import DataLoader
# Qt
from PySide6.QtCore import QStringListModel


class FileModel(QStringListModel):
    """Represents a set of compatible data files."""

    def __init__(self):
        super().__init__()
        self.qualified = {}

    def apply_file_filter(self, dir_path: Path):
        """Applies user-defined filter to generate a list of qualified
        files.

        Qualified files are stored in a dictionary such that the key = filename,
        and value = absolute path.
        """

        # Clear previously-qualified files every time this filter is reapplied
        self.qualified.clear()

        # Find files that meet user qualifications
        for f in dir_path.iterdir():
            if DataLoader().qualify(f):
                self.qualified[f.stem] = str(f)

        # Populate list with newly qualified files
        self.setStringList(self.qualified.keys())

    def name_to_path(self, filename: str) -> Path:
        """Converts filename (key) to absolute path (value)."""

        filepath = self.qualified.get(filename)
        return Path(filepath)