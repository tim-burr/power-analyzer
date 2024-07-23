# Imports
from math import floor, ceil
# Qt
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QWidget
# Graphing toolkit
from pyqtgraph import PlotWidget


class DataViewModel(QObject):
    """Handles analysis view updates."""

    ### Signals ###
    dataSlice = Signal(list)  # Emits slice of plot data for stats calculation


    ### Constructors ###
    def __init__(self, graph: PlotWidget, stats: QWidget):
        super().__init__()
        self._graph = graph
        self._stats = stats
        self.data = []  # Buffer plot data once to avoid retrievals from view

        # Set signal/slot connections
        self._graph.sigRangeChanged.connect(self.refresh_stats)

    def init_views(self, data: list, stats: list):
        """Initializes a graph view and all associated statistic indicators.

        Args:
            data: A list of data of any size.
            stats: A list of any number of statistic dictionaries.
        """

        self._update_graph(data)

        for stat in stats:
            self._stats.add_stat(stat)


    ### Functions ###
    def _update_graph(self, data: list):
        self._graph.getPlotItem().clearPlots()
        self._graph.getPlotItem().plot(y=data)
        self._graph.getPlotItem().autoRange()

        # Not used: Limit zoomed plot scales
        """
        # Define viewbox scale limits
        margin = 1.01  # 1%

        xMin = 0
        xMax = len(data)

        yMin = min(data)
        yMax = max(data)
        yRange = abs(yMax - yMin) * margin
        yMinMargin = yMin - yRange
        yMaxMargin = yMax + yRange

        # Bound zooming out to full data scale
        self._graph.getPlotItem().setLimits(
            xMin = xMin, xMax = xMax,
            yMin = yMinMargin, yMax = yMaxMargin
        )

        # Reset viewbox scales for new data
        self._graph.getPlotItem().setXRange(min=xMin, max=xMax)
        self._graph.getPlotItem().setYRange(min=yMin, max=yMax)
        """

    def _update_stats(self, stats: list[dict]):
        indicators = self._stats.indicators

        for stat in stats:
            index = stat.get('name')
            value = stat.get('value')

            indicators[index].clear()
            indicators[index].setText(f"{value:.3e}")  # Scientific notation

    ### Signals ###
    def refresh_stats(self):
        """Emits signal if stats are out-of-date for a graph."""

        # Calculate uncoerced x-axis bounds for visible plot area
        left_index_raw = int(floor(self._graph.viewRect().left()))
        right_index_raw = int(ceil(self._graph.viewRect().right()))

        # Coerce plot indices to actual data set
        left_index = max(0, left_index_raw)
        right_index = min(right_index_raw, len(self.data)-1)

        # Retrieve and emit data slice
        slice = self.data[left_index:right_index]
        self.dataSlice.emit(slice)


    ### Slots ###
    def update_views(self, values: dict):
        """Updates graph and statistic views with received data.

        Args:
            values: A dictionary containing all raw values and stats for a data set.
        """

        self.data = values.get('data')
        stats = values.get('stats')

        self._update_graph(self.data)
        self._update_stats(stats)