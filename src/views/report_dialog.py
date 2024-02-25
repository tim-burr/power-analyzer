# Imports
from pathlib import Path
# Qt
from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QWidget, QFileDialog
from PySide6.QtGui import QPixmap, QPainter, QRegion


class ReportDialog(QFileDialog):
    """Dialog window for saving an image of an application view.

    The view to be saved is passed in by a parent view reference.
    """

    def __init__(self, parent: QWidget):
        super().__init__()
        self._parent = parent

    def save_img(self, dir: Path):
        """Saves a screenshot of the analysis pane.

        The image is a capture of the view size at the time of saving.

        Args:
            dir: A Path object that represents a save location
            in the filesystem.
        """

        # Get a file path from the user
        dir_path = f"{dir}/Report.png"

        filepath, _ = self.getSaveFileName(
            self._parent, "Save Image", dir_path,
            "Image Files (*.png *.jpg *.bmp)"
        )

        if filepath:
            # Create fixed-sized QPixmap
            #pixmap_width = 1200  #pixels
            #pixmap_height = 700  #pixels
            #pixmap = QPixmap(pixmap_width, pixmap_height)

            # Calculate the self._parent's size and position
            rect = self._parent.rect()
            pixmap = QPixmap(rect.size())
            #scale_width = pixmap_width / rect.width()
            #scale_height = pixmap_height / rect.height()

            # Create QPainter to render the QPixmap
            #painter = QPainter(pixmap)
            #painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            #painter.scale(scale_width, scale_height)
            #painter.translate(-rect.x(), -rect.y())

            # Render the self._parent on the QPixmap
            #self._parent.render(painter)
            self._parent.render(pixmap)
            #painter.end()

            # Save the rendered self._parent as the specified file
            pixmap.save(filepath)