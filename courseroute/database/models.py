# courseroute/database/models.py

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

Base = declarative_base()

# Association tables for many-to-many relationships
student_courses = Table('student_courses', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('course_id', Integer, ForeignKey('courses.id'))
)

student_preferences = Table('student_preferences', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('course_id', Integer, ForeignKey('courses.id'))
)

course_prerequisites = Table('course_prerequisites', Base.metadata,
    Column('course_id', Integer, ForeignKey('courses.id')),
    Column('prerequisite_id', Integer, ForeignKey('courses.id'))
)

teacher_qualifications = Table('teacher_qualifications', Base.metadata,
    Column('teacher_id', Integer, ForeignKey('teachers.id')),
    Column('course_id', Integer, ForeignKey('courses.id'))
)

teacher_availability = Table('teacher_availability', Base.metadata,
    Column('teacher_id', Integer, ForeignKey('teachers.id')),
    Column('timeslot_id', Integer, ForeignKey('timeslots.id'))
)

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    grade_level = Column(Integer)
    completed_courses = relationship('Course', secondary=student_courses)
    preferences = relationship('Course', secondary=student_preferences)
    # Additional fields as needed

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    subject = Column(String)
    credits = Column(Integer)
    prerequisites = relationship('Course', secondary=course_prerequisites,
                                 primaryjoin='Course.id==course_prerequisites.c.course_id',
                                 secondaryjoin='Course.id==course_prerequisites.c.prerequisite_id')
    sections = relationship('CourseSection', back_populates='course')
    # Additional fields as needed

class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    qualifications = relationship('Course', secondary=teacher_qualifications)
    availability = relationship('TimeSlot', secondary=teacher_availability)
    # Additional fields as needed

class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    capacity = Column(Integer)
    special_equipment = Column(String)
    # Additional fields as needed

class TimeSlot(Base):
    __tablename__ = 'timeslots'

    id = Column(Integer, primary_key=True)
    period = Column(Integer)
    day = Column(Integer)
    # Additional fields as needed

class CourseSection(Base):
    __tablename__ = 'course_sections'

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'))
    section_number = Column(Integer)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    timeslot_id = Column(Integer, ForeignKey('timeslots.id'))
    room_id = Column(Integer, ForeignKey('rooms.id'))

    course = relationship('Course', back_populates='sections')
    teacher = relationship('Teacher')
    timeslot = relationship('TimeSlot')
    room = relationship('Room')
