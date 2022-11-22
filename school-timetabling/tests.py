from domain import Timeslot, Room, Lesson, TimeTable
from constraints import define_constraints, room_conflict, teacher_conflict, student_group_conflict, \
    teacher_room_stability, teacher_time_efficiency, student_group_subject_variety

from datetime import time
from optapy.test import ConstraintVerifier, constraint_verifier_build

constraint_verifier: ConstraintVerifier = constraint_verifier_build(define_constraints, TimeTable, Lesson)

ROOM1 = Room(1, "Room1")
ROOM2 = Room(2, "Room2")
TIMESLOT1 = Timeslot(1, 'MONDAY', time(12, 0), time(13, 0))
TIMESLOT2 = Timeslot(2, 'TUESDAY', time(12, 0), time(13, 0))
TIMESLOT3 = Timeslot(3, 'TUESDAY', time(13, 0), time(14, 0))
TIMESLOT4 = Timeslot(4, 'TUESDAY', time(15, 0), time(16, 0))


def test_room_conflict():
    first_lesson = Lesson(1, "Subject1", "Teacher1", "Group1", TIMESLOT1, ROOM1)
    conflicting_lesson = Lesson(2, "Subject2", "Teacher2", "Group2", TIMESLOT1, ROOM1)
    non_conflicting_lesson = Lesson(3, "Subject3", "Teacher3", "Group3", TIMESLOT2, ROOM1)
    constraint_verifier.verify_that(room_conflict) \
        .given(first_lesson, conflicting_lesson, non_conflicting_lesson) \
        .penalizes_by(1)


def test_teacher_conflict():
    conflicting_teacher = "Teacher1"
    first_lesson = Lesson(1, "Subject1", conflicting_teacher, "Group1", TIMESLOT1, ROOM1)
    conflicting_lesson = Lesson(2, "Subject2", conflicting_teacher, "Group2", TIMESLOT1, ROOM2)
    non_conflicting_lesson = Lesson(3, "Subject3", "Teacher2", "Group3", TIMESLOT2, ROOM1)
    constraint_verifier.verify_that(teacher_conflict) \
        .given(first_lesson, conflicting_lesson, non_conflicting_lesson) \
        .penalizes_by(1)


def test_student_group_conflict():
    conflicting_group = "Group1"
    first_lesson = Lesson(1, "Subject1", "Teacher1", conflicting_group, TIMESLOT1, ROOM1)
    conflicting_lesson = Lesson(2, "Subject2", "Teacher2", conflicting_group, TIMESLOT1, ROOM2)
    non_conflicting_lesson = Lesson(3, "Subject3", "Teacher3", "Group3", TIMESLOT2, ROOM1)
    constraint_verifier.verify_that(student_group_conflict) \
        .given(first_lesson, conflicting_lesson, non_conflicting_lesson) \
        .penalizes_by(1)


def test_teacher_room_stability():
    teacher = "Teacher1"
    lesson_in_first_room = Lesson(1, "Subject1", teacher, "Group1", TIMESLOT1, ROOM1)
    lesson_in_same_room = Lesson(2, "Subject2", teacher, "Group2", TIMESLOT1, ROOM1)
    lesson_in_different_room = Lesson(3, "Subject3", teacher, "Group3", TIMESLOT1, ROOM2)
    constraint_verifier.verify_that(teacher_room_stability) \
        .given(lesson_in_first_room, lesson_in_different_room, lesson_in_same_room) \
        .penalizes_by(2)


def test_teacher_time_efficiency():
    teacher = "Teacher1"
    single_lesson_on_monday = Lesson(1, "Subject1", teacher, "Group1", TIMESLOT1, ROOM1)
    first_tuesday_lesson = Lesson(2, "Subject2", teacher, "Group2", TIMESLOT2, ROOM1)
    second_tuesday_lesson = Lesson(3, "Subject3", teacher, "Group3", TIMESLOT3, ROOM1)
    third_tuesday_lesson_with_gap = Lesson(4, "Subject4", teacher, "Group4", TIMESLOT4, ROOM1)
    constraint_verifier.verify_that(teacher_time_efficiency) \
        .given(single_lesson_on_monday, first_tuesday_lesson, second_tuesday_lesson, third_tuesday_lesson_with_gap) \
        .rewards_with(1)  # Second tuesday lesson immediately follows the first.


def test_student_group_subject_variety():
    student_group = "Group1"
    repeated_subject = "Subject1"
    monday_lesson = Lesson(1, repeated_subject, "Teacher1", student_group, TIMESLOT1, ROOM1)
    first_tuesday_lesson = Lesson(2, repeated_subject, "Teacher2", student_group, TIMESLOT2, ROOM1)
    second_tuesday_lesson = Lesson(3, repeated_subject, "Teacher3", student_group, TIMESLOT3, ROOM1)
    third_tuesday_lesson_with_different_subject = Lesson(4, "Subject2", "Teacher4", student_group, TIMESLOT4, ROOM1)
    lesson_in_another_group = Lesson(5, repeated_subject, "Teacher5", "Group2", TIMESLOT1, ROOM1)
    constraint_verifier.verify_that(student_group_subject_variety) \
        .given(monday_lesson, first_tuesday_lesson, second_tuesday_lesson, third_tuesday_lesson_with_different_subject,
               lesson_in_another_group) \
        .penalizes_by(1)  # Second tuesday lesson immediately follows the first.
