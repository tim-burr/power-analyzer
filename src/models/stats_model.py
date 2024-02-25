# Imports
import numpy as np
from scipy.signal import find_peaks


class StatsModel():
    """Calculates statistics for a user-defined data list.

    Statistics are calculated once at class initialization and then buffered
    for as long as the class instance exists.

    Attributes:
        stats: A list of statistic dictionaries. Dictionaries are uniformly
            formatted to contain 'name,' 'value,' and 'unit' entries.
    """

    def __init__(self, data: list = [0], unit: str = ""):
        self.stats = []
        self._calc_stats(data, unit)

    def _calc_freq(self, data: list, fs: int) -> np.intp:
        """Single-sided, peak-detect FFT."""

        fourier = np.abs(np.fft.rfft(data))
        freqs = np.fft.rfftfreq(len(data), d=1/fs)

        # Find peaks in the spectrum
        peaks, _ = find_peaks(fourier)
        peak_freqs = freqs[peaks]

        # Identify dominant normalized frequencies
        norm_magnitudes = fourier[peaks] / np.max(fourier)

        if norm_magnitudes.any():
            dominant_freq = peak_freqs[np.argmax(norm_magnitudes)]
        else:
            dominant_freq = 0  # No dominant frequency

        return dominant_freq

    def _calc_stats(self, data: list, unit: str):
        if not data:
            return

        # Calculate base stats
        min_peak = min(data)
        max_peak = max(data)
        delta = abs(max_peak-min_peak)
        std_dev = np.std(data)
        freq = self._calc_freq(data, fs=1000)  # 1 kHz sample rate

        # Structure stats into a list of dicts
        stats = [
            {'name': "Min Peak",      'value': min_peak,  'unit': unit},
            {'name': "Max Peak",      'value': max_peak,  'unit': unit},
            {'name': "Delta Peaks",   'value': delta,     'unit': unit},
            {'name': "RMS Noise",     'value': std_dev,   'unit': unit},
            {'name': "Pk-Pk Noise",   'value': std_dev*6, 'unit': unit},
            {'name': "Dominant Freq", 'value': freq,      'unit': "Hz"},
        ]
        self.stats = stats