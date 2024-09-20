# courseroute/gui/main_window.py

from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtCore import pyqtSlot
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
        # In __init__ method of MainWindow

        self.ui.addStudentButton.clicked.connect(self.open_add_student_form)
        self.ui.editStudentButton.clicked.connect(self.open_edit_student_form)
        self.ui.deleteStudentButton.clicked.connect(self.delete_student)
        # Repeat for courses, teachers, rooms
        
        # Menu actions for import/export
        self.ui.actionImport_PowerSchool.triggered.connect(self.import_powerschool_data)
        self.ui.actionExport_PowerSchool.triggered.connect(self.export_to_powerschool)

        # Connect menu actions
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionImport_Data.triggered.connect(self.import_data)
        self.ui.actionExport_Schedule.triggered.connect(self.export_schedule)

        # Connect buttons
        self.ui.runSchedulerButton.clicked.connect(self.run_scheduler)
        self.ui.addStudentButton.clicked.connect(self.open_add_student_form)
        # Initialize data views
        self.load_data_views()

    def load_data_views(self):
        # Load data into tables (students, courses, teachers, etc.)
        pass

    @pyqtSlot()
    def run_scheduler(self):
        # Run the selected scheduling algorithm
        scheduler_type = self.ui.schedulerComboBox.currentText()
        if scheduler_type == "ILP Scheduler":
            schedule = generate_schedule_ilp(self.session)
        else:
            schedule = generate_schedule_genetic(self.session)

        if schedule:
            self.display_schedule(schedule)
        else:
            QMessageBox.warning(self, "Scheduling Error", "Could not generate schedule.")

    # In display_schedule method

    def display_schedule(self, schedule):
        self.ui.scheduleTableWidget.clearContents()
        self.ui.scheduleTableWidget.setRowCount(0)
        headers = ["Student ID", "Student Name", "Course", "Section", "Time Slot", "Teacher", "Room"]
        self.ui.scheduleTableWidget.setColumnCount(len(headers))
        self.ui.scheduleTableWidget.setHorizontalHeaderLabels(headers)
    
        for student_id, courses in schedule.items():
            student = self.session.query(Student).get(student_id)
            for course_info in courses:
                row_position = self.ui.scheduleTableWidget.rowCount()
                self.ui.scheduleTableWidget.insertRow(row_position)
                self.ui.scheduleTableWidget.setItem(row_position, 0, QTableWidgetItem(str(student_id)))
                self.ui.scheduleTableWidget.setItem(row_position, 1, QTableWidgetItem(student.name))
                self.ui.scheduleTableWidget.setItem(row_position, 2, QTableWidgetItem(course_info['course']))
                self.ui.scheduleTableWidget.setItem(row_position, 3, QTableWidgetItem(str(course_info['section'])))
                self.ui.scheduleTableWidget.setItem(row_position, 4, QTableWidgetItem(str(course_info['timeslot'])))
                self.ui.scheduleTableWidget.setItem(row_position, 5, QTableWidgetItem(course_info['teacher']))
                self.ui.scheduleTableWidget.setItem(row_position, 6, QTableWidgetItem(course_info['room']))


    @pyqtSlot()
    def import_data(self):
        # Implement data import functionality
        file_name, _ = QFileDialog.getOpenFileName(self, "Import Data", "", "CSV Files (*.csv);;All Files (*)")
        if file_name:
            # Read the CSV file and populate the database
            pass

    @pyqtSlot()
    def export_schedule(self):
        # Implement schedule export functionality
        file_name, _ = QFileDialog.getSaveFileName(self, "Export Schedule", "", "CSV Files (*.csv);;All Files (*)")
        if file_name:
            # Write the schedule to the CSV file
            pass
            
    def open_add_student_form(self):
        from courseroute.gui.student_form import StudentForm
        dialog = StudentForm(self)
        if dialog.exec_():
            self.load_students()

    def load_students(self):
        # Load student data into the student table
        pass

    def delete_student(self):
        selected_items = self.ui.studentTableWidget.selectedItems()
        if selected_items:
            student_id = selected_items[0].text()
            student = self.session.query(Student).get(student_id)
            if student:
                self.session.delete(student)
                self.session.commit()
                self.load_students()
                
    def import_powerschool_data(self):
        from courseroute.integrations.powerschool_api import import_data_from_powerschool
        import_data_from_powerschool(self.session)
        self.load_all_data()
    
