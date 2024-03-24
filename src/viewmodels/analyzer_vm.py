# Imports
from pathlib import Path
from utilities.data_loader import DataLoader
from viewmodels.data_vm import DataViewModel
from models.stats_model import StatsModel
from views.report_dialog import ReportDialog
# Qt
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QWidget, QPushButton


class AnalyzerViewModel(QObject):
    """Dispatches model values to multiple data view-model instances."""

    ### Signals ###
    voltageChanged = Signal(dict)  # Emits new voltage data and stats
    currentChanged = Signal(dict)  # Emits new current data and stats


    ### Constructors ###
    def __init__(self, button: QPushButton, voltage: QWidget, current: QWidget):
        super().__init__()
        self._button = button
        self._voltage_vm: DataViewModel = voltage.viewmodel
        self._current_vm: DataViewModel = current.viewmodel
        self._data_loader = DataLoader()
        self._dir: Path = ''
        self._init_views()

        # Set signal/slot connections
        self._button.clicked.connect(self._save_img)
        self.voltageChanged.connect(self._voltage_vm.update_views)
        self.currentChanged.connect(self._current_vm.update_views)

    def _init_views(self):
        default_data = [0,1]
        voltage_stats = StatsModel(default_data, "V").stats
        current_stats = StatsModel(default_data, "A").stats

        self._voltage_vm.init_views(default_data, voltage_stats)
        self._current_vm.init_views(default_data, current_stats)


    ### Slots ###
    def update_views(self, fpath: Path):
        """Emits new data and stats upon a successful file load.

        Args:
            fpath: A Path object that points to a user data file.
        """

        if fpath.is_file():
            self._dir = fpath.parent  # Set the active data directory
            all_data = self._data_loader.load(fpath)
        else:
            return  # Not a valid file path

        # Buffer named data lists
        voltage_data = list(all_data[DataLoader.KEYS[0]])
        current_data = list(all_data[DataLoader.KEYS[1]])

        # Calculate stats from data lists
        voltage_stats = StatsModel(voltage_data, "V").stats
        current_stats = StatsModel(current_data, "A").stats

        # Notify external module that new data and stats are available
        self.voltageChanged.emit({'data': voltage_data,
                                  'stats': voltage_stats})
        self.currentChanged.emit({'data': current_data,
                                  'stats': current_stats})

    def _save_img(self):
        dialog = ReportDialog(parent=self._button.parent())
        dialog.save_img(dir=self._dir)