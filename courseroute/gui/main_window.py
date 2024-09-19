# courseroute/gui/main_window.py

from PyQt5.QtWidgets import QMainWindow, QMessageBox
from courseroute.gui.ui.main_window_ui import Ui_MainWindow
from courseroute.database.db_manager import create_session
from courseroute.algorithms.ilp_scheduler import generate_schedule_ilp
from courseroute.algorithms.genetic_scheduler import generate_schedule_genetic

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.session = create_session()
        self.ui.runIlpButton.clicked.connect(self.run_ilp_scheduler)
        self.ui.runGeneticButton.clicked.connect(self.run_genetic_scheduler)
        # Additional initialization

    def run_ilp_scheduler(self):
        schedule = generate_schedule_ilp(self.session)
        if schedule:
            self.display_schedule(schedule)
        else:
            QMessageBox.warning(self, "Scheduling Error", "Could not generate schedule using ILP.")

    def run_genetic_scheduler(self):
        schedule = generate_schedule_genetic(self.session)
        if schedule:
            self.display_schedule(schedule)
        else:
            QMessageBox.warning(self, "Scheduling Error", "Could not generate schedule using Genetic Algorithm.")

    def display_schedule(self, schedule):
        # Implement code to display the schedule in the GUI
        # For example, populate a table or export to a file
        pass
