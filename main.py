from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QMainWindow,
    QWidget,
    QApplication,
    QFileDialog,
)

from config import Config
from eeg_plot import EEGPlot
from control_frame import ControlToolBar
from eeg_frame import EEGPlotWidget

config = Config()


class EEGAnnotator(QMainWindow):
    """EEG Annotator main window"""

    def __init__(self):
        super(EEGAnnotator, self).__init__()
        self.setWindowTitle("EEG Annotator")
        self.resize(1024, 720)
        self.eep = EEGPlot()
        self.signal_duration = None

        layout = QHBoxLayout()
        self.control_toolbar = ControlToolBar(self)
        self.eeg_plot_widget = EEGPlotWidget(self, self.eep)

        # add toolbar
        self.addToolBar(self.control_toolbar)
        menu = self.menuBar()
        # create an open action
        openAction = QAction("Open", self)
        openAction.triggered.connect(self.open_file)

        # Add the open action to the menu
        fileMenu = menu.addMenu("&File")
        fileMenu.addAction(openAction)

        # add widgets to the layout
        layout.addWidget(self.eeg_plot_widget)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def open_file(self):
        self.eeg_plot_widget.fig.clear()
        # Open a file dialog
        self.filename = QFileDialog.getOpenFileName(self)[0]

        if not self.filename:
            return

        if self.filename.lower().strip().endswith(".edf"):
            self.raw_eeg, self.signal_duration = self.eep.read_edf(
                self.filename.strip(), config.montage_pairs
            )

        if self.filename.lower().strip().endswith(".eeg"):
            self.raw_eeg, self.signal_duration = self.eep.read_eeg(
                self.filename.strip(), config.montage_pairs
            )

        if self.raw_eeg:
            self.control_toolbar.draw_selection_btn.setEnabled(True)
            self.control_toolbar.show_controls(self.signal_duration)
            self.eeg_plot_widget.show_plot(self.raw_eeg, self.signal_duration)


app = QApplication([])
window = EEGAnnotator()
window.show()

app.exec()
