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
from datetime import datetime


class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLabel(text='Time', units=None)
        self.enableAutoSIPrefix(False)

    def tickStrings(self, values, scale, spacing):
        return [datetime.fromtimestamp(value).strftime("%M:%S.%f")[:-3] for value in values]


class MainWindow(QMainWindow):

    def __init__(self, file_path: str):
        super(MainWindow, self).__init__()

        string_format = "%Y-%d-%m %H:%M:%S.%f"

        self.setWindowTitle("Display Acceleration")
        self.setMinimumSize(800, 600)

        # Create Graph
        self.graph = pg.PlotWidget(axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        layout = QGridLayout()
        layout.addWidget(self.graph, 0, 0, 2, 2)

        self.button = QPushButton("Start")
        # self.button.clicked.connect(self.start_stop)

        layout.addWidget(self.button, 2, 1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.graph.setBackground("w")

        self.graph.setTitle("Acceleration Data", color='b', size='20pt')
        styles = {"color": "red", "font-size": "18px"}
        self.graph.setLabel("left", "Value", **styles)
        self.graph.setLabel("bottom", "Time", **styles)
        self.graph.addLegend()
        self.graph.showGrid(x=True, y=True)

        self.date_time = []
        self.x_ddot = []
        self.y_ddot = []
        self.z_ddot = []
        # read data
        with open(file_path, 'r') as f:
            data = f.readlines()
        for line in data:
            values = line.split(',')
            self.date_time.append(datetime.strptime(values[0], string_format))
            self.x_ddot.append(float(values[1]))
            self.y_ddot.append(float(values[2]))
            self.z_ddot.append(float(values[3][:-1]))

        self.time = [dt.timestamp() for dt in self.date_time]
        pen_width = 5
        pen = pg.mkPen(color="blue", width=pen_width)
        self.graph.plot(
            self.time,
            self.x_ddot,
            name="X Acceleration",
            pen=pen,
        )
        pen = pg.mkPen(color="green", width=pen_width)
        self.graph.plot(
            self.time,
            self.y_ddot,
            name="Y Acceleration",
            pen=pen,
        )
        pen = pg.mkPen(color="red", width=pen_width)
        self.graph.plot(
            self.time,
            self.z_ddot,
            name="Z Acceleration",
            pen=pen,
        )

        self.graph.setMouseEnabled(x=False, y=False)
        self.graph.hideButtons()
        self.graph.getPlotItem().setMenuEnabled(False)

        legend = self.graph.addLegend()
        legend.setOffset((0, 0))
        legend.mouseDragEvent = lambda *args, **kwargs: None
        legend.hoverEvent = lambda *args, **kwargs: None

        # add timer
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)

    def update_plot(self):
        pass

    def start_stop(self):
        if self.timer.isActive():
            self.timer.stop()
            self.button.setText("Start")
        else:
            self.timer.start()
            self.button.setText("Stop")


app = QApplication(sys.argv)
w = MainWindow("data/07-08_17-57-53_accel.csv")
w.show()
app.exec()
