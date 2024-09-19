# eduscheduler/algorithms/ilp_scheduler.py

import pulp
from eduscheduler.database.models import Student, CourseSection, TimeSlot, Teacher
from sqlalchemy.orm import Session

def generate_schedule_ilp(session: Session):
    # Fetch data from the database
    students = session.query(Student).all()
    course_sections = session.query(CourseSection).all()
    timeslots = session.query(TimeSlot).all()
    teachers = session.query(Teacher).all()

    # Initialize the ILP problem
    prob = pulp.LpProblem("HighSchoolScheduling", pulp.LpMaximize)

    # Decision variables
    x = {}
    for student in students:
        for cs in course_sections:
            var_name = f"x_{student.id}_{cs.id}"
            x[(student.id, cs.id)] = pulp.LpVariable(var_name, cat='Binary')

    # Constraints

    # Constraint: Each student is assigned to the required number of courses
    for student in students:
        required_courses = get_required_courses_per_student(student)
        prob += (
            pulp.lpSum(x[(student.id, cs.id)] for cs in course_sections) == required_courses,
            f"Student_{student.id}_CourseLoad"
        )

    # Constraint: No time conflicts for students
    for student in students:
        for timeslot in timeslots:
            prob += (
                pulp.lpSum(
                    x[(student.id, cs.id)] for cs in course_sections if cs.timeslot_id == timeslot.id
                ) <= 1,
                f"Student_{student.id}_Timeslot_{timeslot.id}_Conflict"
            )

    # Constraint: Prerequisites are met
    for student in students:
        completed_course_ids = [course.id for course in student.completed_courses]
        for cs in course_sections:
            required_prereq_ids = [prereq.id for prereq in cs.course.prerequisites]
            if not set(required_prereq_ids).issubset(set(completed_course_ids)):
                prob += (
                    x[(student.id, cs.id)] == 0,
                    f"Student_{student.id}_Course_{cs.course.id}_Prerequisite"
                )

    # Constraint: Room capacities are not exceeded
    for cs in course_sections:
        room_capacity = cs.room.capacity
        prob += (
            pulp.lpSum(
                x[(student.id, cs.id)] for student in students
            ) <= room_capacity,
            f"Section_{cs.id}_RoomCapacity"
        )

    # Constraint: Teacher availability
    for teacher in teachers:
        teacher_sections = [cs for cs in course_sections if cs.teacher_id == teacher.id]
        for timeslot in timeslots:
            if timeslot not in teacher.availability:
                for cs in teacher_sections:
                    if cs.timeslot_id == timeslot.id:
                        prob += (
                            pulp.lpSum(
                                x[(student.id, cs.id)] for student in students
                            ) == 0,
                            f"Teacher_{teacher.id}_Timeslot_{timeslot.id}_Unavailable"
                        )
            else:
                prob += (
                    pulp.lpSum(
                        x[(student.id, cs.id)] for student in students for cs in teacher_sections if cs.timeslot_id == timeslot.id
                    ) <= cs.room.capacity,
                    f"Teacher_{teacher.id}_Timeslot_{timeslot.id}_Conflict"
                )

    # Objective Function: Maximize student preferences
    prob += (
        pulp.lpSum(
            x[(student.id, cs.id)] * preference_weight(student, cs.course)
            for student in students
            for cs in course_sections
        ),
        "Total_Preference_Satisfaction"
    )

    # Solve the problem
    prob.solve()

    # Check the status
    if pulp.LpStatus[prob.status] == 'Optimal':
        schedule = {}
        for student in students:
            student_schedule = []
            for cs in course_sections:
                if pulp.value(x[(student.id, cs.id)]) == 1:
                    student_schedule.append({
                        'course': cs.course.name,
                        'section': cs.section_number,
                        'timeslot': cs.timeslot.period,
                        'teacher': cs.teacher.name,
                        'room': cs.room.name
                    })
            schedule[student.id] = student_schedule
        return schedule
    else:
        print("No optimal solution found.")
        return None

def preference_weight(student, course):
    if course in student.preferences:
        rank = student.preferences.index(course)
        return len(student.preferences) - rank
    else:
        return 0

def get_required_courses_per_student(student):
    # Return the number of courses each student should be enrolled in
    return 7  # Example value
