#!/usr/bin/env python3

# Imports
import sys
from views.style import Style
from views.window_view import Window
# Qt
from PySide6.QtWidgets import QApplication


"""Main program for analyzing user data."""
__author__ = "Timothy Burroughs"

def launch():
    app = QApplication([])
    Style(app)
    window = Window()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    launch()