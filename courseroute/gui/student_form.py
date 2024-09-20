# courseroute/gui/student_form.py

from PyQt5.QtWidgets import QDialog
from courseroute.gui.ui.student_form_ui import Ui_StudentForm
from courseroute.database.models import Student
from courseroute.database.db_manager import create_session

class StudentForm(QDialog):
    def __init__(self, parent=None, student=None):
        super().__init__(parent)
        self.ui = Ui_StudentForm()
        self.ui.setupUi(self)
        self.session = create_session()
        self.student = student

        if self.student:
            self.load_student_data()

        self.ui.saveButton.clicked.connect(self.save_student)
        self.ui.cancelButton.clicked.connect(self.reject)

    def load_student_data(self):
        self.ui.studentNameLineEdit.setText(self.student.name)
        self.ui.gradeLevelSpinBox.setValue(self.student.grade_level)
        # Load other fields as necessary

    def save_student(self):
        name = self.ui.studentNameLineEdit.text()
        grade_level = self.ui.gradeLevelSpinBox.value()
        # Retrieve other fields

        if not self.student:
            self.student = Student()

        self.student.name = name
        self.student.grade_level = grade_level
        # Set other fields

        self.session.add(self.student)
        self.session.commit()
        self.accept()
