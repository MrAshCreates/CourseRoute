# eduscheduler/algorithms/genetic_scheduler.py

import numpy as np
import pygad
from eduscheduler.database.models import Student, CourseSection
from sqlalchemy.orm import Session

def generate_schedule_genetic(session: Session):
    # Fetch data from the database
    students = session.query(Student).all()
    course_sections = session.query(CourseSection).all()
    
    num_students = len(students)
    num_sections = len(course_sections)
    courses_per_student = get_courses_per_student()
    chromosome_length = num_students * courses_per_student

    # Map course sections to indices
    cs_indices = {i: cs for i, cs in enumerate(course_sections)}

    # Define the fitness function
    def fitness_func(solution, solution_idx):
        fitness = 0
        solution = solution.astype(int)
        # Decode the solution and calculate fitness
        for i in range(num_students):
            student = students[i]
            assigned_sections_indices = solution[i*courses_per_student:(i+1)*courses_per_student]
            assigned_sections = [cs_indices[idx] for idx in assigned_sections_indices]

            # Check for time conflicts
            timeslots = [cs.timeslot_id for cs in assigned_sections]
            if len(timeslots) != len(set(timeslots)):
                fitness -= 10  # Penalty for time conflicts

            # Check prerequisites
            for cs in assigned_sections:
                required_prereq_ids = [prereq.id for prereq in cs.course.prerequisites]
                completed_course_ids = [course.id for course in student.completed_courses]
                if not set(required_prereq_ids).issubset(set(completed_course_ids)):
                    fitness -= 5  # Penalty for missing prerequisites

            # Preferences
            for cs in assigned_sections:
                fitness += preference_weight(student, cs.course)

        return fitness

    # Set up PyGAD parameters
    ga_instance = pygad.GA(
        num_generations=100,
        num_parents_mating=10,
        fitness_func=fitness_func,
        sol_per_pop=50,
        num_genes=chromosome_length,
        gene_type=int,
        gene_space={'low': 0, 'high': num_sections - 1},
        allow_duplicate_genes=False
    )

    # Run the genetic algorithm
    ga_instance.run()

    # Retrieve the best solution
    solution, solution_fitness, solution_idx = ga_instance.best_solution()

    # Decode the solution into a schedule
    schedule = {}
    for i in range(num_students):
        student = students[i]
        assigned_sections_indices = solution[i*courses_per_student:(i+1)*courses_per_student]
        assigned_sections = [cs_indices[idx] for idx in assigned_sections_indices]
        student_schedule = []
        for cs in assigned_sections:
            student_schedule.append({
                'course': cs.course.name,
                'section': cs.section_number,
                'timeslot': cs.timeslot.period,
                'teacher': cs.teacher.name,
                'room': cs.room.name
            })
        schedule[student.id] = student_schedule

    return schedule

def preference_weight(student, course):
    if course in student.preferences:
        rank = student.preferences.index(course)
        return len(student.preferences) - rank
    else:
        return 0

def get_courses_per_student():
    # Return the number of courses each student should be enrolled in
    return 7  # Example value
