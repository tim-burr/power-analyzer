# Imports
from viewmodels.disk_vm import DiskViewModel
from viewmodels.analyzer_vm import AnalyzerViewModel
# Qt
from PySide6.QtCore import QObject


class Mediator(QObject):
    """Bridges data flow between independent application features.

    Supported Features:
        Filesystem navigation,
        Data analysis,
    """

    def __init__(self, nav_viewmodel: DiskViewModel,
                 analyzer_viewmodel: AnalyzerViewModel):
        super().__init__()

        # Connect new file path to data view-model
        nav_viewmodel.newPath.connect(analyzer_viewmodel.update_views)