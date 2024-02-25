# Imports
from viewmodels.analyzer_vm import AnalyzerViewModel
from viewmodels.data_vm import DataViewModel
# Qt
from PySide6.QtWidgets import (
    QWidget, QPushButton, QLabel, QLineEdit,
    QGridLayout
)
# Graphing toolkit
from pyqtgraph import PlotWidget


class DescriptionBox(QLineEdit):
    """Accepts a test description from the user during runtime."""

    def __init__(self):
        super().__init__()
        self._build()

    def _build(self):
        self.setPlaceholderText("Enter test description...")


class Graph(PlotWidget):
    """Data chart that can be manipulated during runtime."""

    def __init__(self, name: str, unit: str):
        super().__init__()
        self._name = name
        self._unit = unit
        self._build()
        self._style()

    def _build(self):
        self.setLabel("left", f"{self._name} ({self._unit})")
        self.setLabel("bottom", "Counts")

    def _style(self):
        # Style sheet syntax not supported for PlotWidget
        gray = (12, 12, 12)
        self.setBackground(gray)
        self.showGrid(y=True)


class Statistics(QWidget):
    """Statistical indicators that update per loaded file.

    Attributes:
        indicators: A dictionary of user-defined statistical indicator subviews.
            This attribute may be updated at both compile and run time.
    """

    class StatIndicator(QLineEdit):
        def __init__(self):
            super().__init__()
            self.setReadOnly(True)

    def __init__(self):
        super().__init__()
        self.indicators = {}
        self._layout = QGridLayout()
        self.setLayout(self._layout)

    def add_stat(self, stat: dict):
        """Adds a new statistic line to the data block view.

        Call to insert a new row of statistical info in the analysis view.
        Fills top to bottom.

        Args:
            stat: A dictionary containing a single stat's name, value, and unit.
        """

        # Extract data from stats
        name = stat['name']
        unit = stat['unit']

        # Find next available row in layout
        next_row = self._layout.rowCount()

        # Add widgets to same row in layout
        self.indicators[name] = self.StatIndicator()
        self._layout.addWidget(QLabel(name), next_row, 0, 1, 1)
        self._layout.addWidget(self.indicators[name], next_row, 1, 1, 2)
        self._layout.addWidget(QLabel(unit), next_row, 3, 1, 1)


class DataBlock(QWidget):
    """Data block for a single set of loaded data.

    Attributes:
        viewmodel: A DataViewModel object, which is the view's assigned model.
    """

    def __init__(self, name: str, unit: str):
        super().__init__()
        self._name = name
        self._unit = unit
        self.viewmodel: DataViewModel
        self._build()

    def _build(self):
        header = QLabel(f"{self._name.title()} Data")
        header.setObjectName("header")  # Enable styling by name
        graph = Graph(self._name, self._unit)
        stats = Statistics()

        self.viewmodel = DataViewModel(graph, stats)

        layout = QGridLayout()
        layout.addWidget(header, 0, 0, 1, 2)
        layout.addWidget(graph, 1, 0)
        layout.addWidget(stats, 1, 1)
        self.setLayout(layout)


class Analyzer(QWidget):
    """Combined analysis pane for all loaded data.

    Attributes:
        viewmodel: A AnalyzerViewModel object, which is the view's assigned model.
    """

    def __init__(self):
        super().__init__()
        self.viewmodel: AnalyzerViewModel
        self._build()

    def _build(self):
        desc_box = DescriptionBox()
        save_button = QPushButton("Save")
        voltage_data = DataBlock(name="Voltage", unit="V")
        current_data = DataBlock(name="Current", unit="A")

        self.viewmodel = AnalyzerViewModel(
            save_button, voltage_data, current_data
        )

        layout = QGridLayout()
        layout.addWidget(desc_box, 0, 0)
        layout.addWidget(save_button, 0, 1)
        layout.addWidget(voltage_data, 1, 0, 1, 2)
        layout.addWidget(current_data, 2, 0, 1, 2)
        self.setLayout(layout)