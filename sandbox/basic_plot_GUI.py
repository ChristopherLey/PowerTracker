import sys

from PyQt6 import QtCore
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QWidget,
    QGridLayout
)
from PyQt6.QtGui import QPalette, QColor
import pyqtgraph as pg
from random import randint


class Colour(QWidget):
    def __init__(self, colour: str):
        super(Colour, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(colour))
        self.setPalette(palette)


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My Colour App")
        self.setMinimumSize(800, 600)

        # Create Graph
        self.graph = pg.PlotWidget()
        layout = QGridLayout()
        layout.addWidget(self.graph, 0, 0, 2, 2)

        self.button = QPushButton("Start")
        self.button.clicked.connect(self.start_stop)

        layout.addWidget(self.button, 2, 1)


        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.graph.setBackground("w")
        pen = pg.mkPen(color=(255, 0, 0))
        self.graph.setTitle("Random Data", color='b', size='20pt')
        styles = {"color": "red", "font-size": "18px"}
        self.graph.setLabel("left", "Value", **styles)
        self.graph.setLabel("bottom", "Time", **styles)
        self.graph.addLegend()
        self.graph.showGrid(x=True, y=True)
        self.graph.setYRange(20, 40)
        self.time = list(range(10))
        self.temperature = [randint(20, 40) for _ in range(10)]
        self.line = self.graph.plot(
            self.time,
            self.temperature,
            name="Temperature",
            pen=pen,
        )

        # add timer
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)

    def update_plot(self):
        self.time = self.time[1:]
        self.time.append(self.time[-1] + 1)
        self.temperature = self.temperature[1:]
        self.temperature.append(randint(20, 40))
        self.line.setData(self.time, self.temperature)

    def start_stop(self):
        if self.timer.isActive():
            self.timer.stop()
            self.button.setText("Start")
        else:
            self.timer.start()
            self.button.setText("Stop")


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
