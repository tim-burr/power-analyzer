# Imports
from pathlib import Path
from pandas import read_csv
import csv


class DataLoader:
    """Provides functions for loading and qualifying individual files.

    Qualification is defined by an external KEYS file that gets read once
    during class initialization.

    Attributes:
        keys: A list global constant that stores user-defined data types.
    """

    ### Constants ###
    KEYS = []  # Keys into model values

    def __init__(self):
        # Load in keys from user template
        with open(Path(__file__).parents[1] / 'data/KEYS.csv', 'r') as f:
            reader = csv.DictReader(f)
            DataLoader.KEYS = reader.fieldnames

    def qualify(self, fpath: str) -> bool:
        """Check if target CSV contains expected header."""

        isCSV = Path(fpath).suffix.lower() == ".csv"

        if not isCSV:
            return False

        try:
            with open(Path(fpath), 'r') as f:
                reader = csv.DictReader(f)
                header = reader.fieldnames

            # Return True if qualifying names are in header
            has_match = header <= DataLoader.KEYS
            return has_match

        except:
            return False

    def load(self, fpath: str = '') -> dict:
        """Load compatible data sets into a dictionary."""

        # Buffer only the relevant columns
        dataframe = read_csv(
            filepath_or_buffer = fpath,
            header = 0,
            usecols = DataLoader.KEYS,
            delimiter = ',',
            dtype = 'float64',
        )

        datadict = dataframe.to_dict(orient='series')
        return datadict