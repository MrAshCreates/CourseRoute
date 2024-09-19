# eduscheduler/gui/ui/main_window_ui.py

from PyQt5 import QtCore, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("EduScheduler")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.runIlpButton = QtWidgets.QPushButton(self.centralwidget)
        self.runIlpButton.setText("Run ILP Scheduler")
        self.runIlpButton.setGeometry(QtCore.QRect(50, 50, 200, 50))
        self.runGeneticButton = QtWidgets.QPushButton(self.centralwidget)
        self.runGeneticButton.setText("Run Genetic Scheduler")
        self.runGeneticButton.setGeometry(QtCore.QRect(50, 120, 200, 50))
        # Add more UI elements as needed
        MainWindow.setCentralWidget(self.centralwidget)
