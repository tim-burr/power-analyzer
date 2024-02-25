# Imports
from pathlib import Path
from models.disk_model import DiskModel
from models.file_model import FileModel
# Qt
from PySide6.QtCore import Qt, QObject, QModelIndex, QDir, Signal
from PySide6.QtWidgets import QLineEdit, QCompleter, QTreeView, QListView


class DiskViewModel(QObject):
    """Handles directory and file navigation events."""

    ### Signals ###
    newPath = Signal(Path)  # Emits new data path to external modules


    ### Constructors ###
    def __init__(self, lineview: QLineEdit, treeview: QTreeView, listview: QListView):
        super().__init__()
        self._lineview = lineview
        self._treeview = treeview
        self._listview = listview
        self._model = DiskModel()

        self._init_line(self._lineview)
        self._init_tree(self._treeview)
        self._init_list(self._listview)

    def _init_line(self, view: QLineEdit):
        completer = QCompleter(view)
        completer.setModel(self._model)
        completer.setCompletionMode(QCompleter.InlineCompletion)
        view.setCompleter(completer)
        # Set signal/slot connections
        view.textChanged.connect(self._line_changed)
        view.editingFinished.connect(self._line_completed)

    def _init_tree(self, view: QTreeView):
        path = QDir.rootPath()
        view.setModel(self._model)
        index = self._model.setRootPath(path)
        view.setRootIndex(index)
        view.format()
        # Set signal/slot connections
        view.selectionModel().currentChanged.connect(self._tree_changed)

    def _init_list(self, view: QListView):
        model = FileModel()
        view.setModel(model)
        # Set signal/slot connections
        view.selectionModel().currentChanged.connect(self._list_changed)


    ### Functions ###
    def _check_line(self, path: Path) -> bool:
        """Called every time the line changes by at least one character."""

        # Retrieve current text color
        current_color = self._lineview.property("textColor")

        # Only allow valid directory paths in the URL box
        if (path.is_file() or not path.exists()):
            new_color = 'invalid'
        else:
            new_color = 'valid'

        # Polish the view only if its text color property changed
        if new_color != current_color:
            self._lineview.setProperty('textColor', new_color)
            self._lineview.style().polish(self._lineview)

        if new_color == 'valid':
            return True
        else:
            return False


    ### Slots ###
    def _line_changed(self):
        """Called after every key stroke."""

        current_path = self._lineview.text()
        valid = self._check_line(Path(current_path))

        if not valid:
            return

        model = self._lineview.completer().model()
        index = model.index(current_path)

        self._treeview.setCurrentIndex(index)

    def _line_completed(self):
        """Called only after the line loses focus and editing is complete."""

        model = self._lineview.completer().model()
        current_path = self._lineview.text()

        model_root = str(Path(model.rootPath()).anchor)
        line_root = str(Path(current_path).anchor)

        # Only change tree root if path in URL box is a different root
        if line_root and Path(line_root).is_dir() and (model_root != line_root):
            index = model.setRootPath(line_root)
            self._treeview.setRootIndex(index)

    def _tree_changed(self, index: QModelIndex):
        """Called after any tree item selection change."""

        if not index.isValid():
            return

        # Get path from model item index
        path = index.model().filePath(index)

        # Sync selected path with directory box
        self._lineview.setText(path)

        # Apply custom file filter to list view
        self._listview.model().apply_file_filter(Path(path))

    def _list_changed(self, index: QModelIndex):
        """Called after any list item selection change."""

        if not index.isValid():
            return

        # Get path from model item index
        filename = index.model().data(index, Qt.DisplayRole)
        filepath = index.model().name_to_path(filename)

        # Emit signal with new path
        self.newPath.emit(filepath)