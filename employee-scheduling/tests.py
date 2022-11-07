from domain import AvailabilityType, Availability, Employee, Shift, EmployeeSchedule
from constraints import employee_scheduling_constraints, required_skill, no_overlapping_shifts, \
    at_least_10_hours_between_two_shifts, desired_day_for_employee, undesired_day_for_employee, unavailable_employee

from optapy.test import ConstraintVerifier, constraint_verifier_build
from datetime import date, time, datetime, timedelta

DAY_1 = date(2021, 2, 1)
DAY_2 = date(2021, 2, 2)
DAY_3 = date(2021, 2, 3)

DAY_START_TIME = datetime.combine(DAY_1, time(9, 0))
DAY_END_TIME = datetime.combine(DAY_1, time(17, 0))
AFTERNOON_START_TIME = datetime.combine(DAY_1, time(13, 0))
AFTERNOON_END_TIME = datetime.combine(DAY_1, time(21, 0))

constraint_verifier: ConstraintVerifier = constraint_verifier_build(employee_scheduling_constraints, EmployeeSchedule,
                                                                    Shift)


def test_required_skill():
    employee = Employee("Amy", [])
    constraint_verifier.verify_that(required_skill) \
        .given(employee,
               Shift(1, DAY_START_TIME, DAY_END_TIME, "Location", "Skill", employee)) \
        .penalizes(1)

    employee = Employee("Beth", ["Skill"])
    constraint_verifier.verify_that(required_skill) \
        .given(employee,
               Shift(1, DAY_START_TIME, DAY_END_TIME, "Location", "Skill", employee)) \
        .penalizes(0)


def test_overlapping_shifts():
    employee1 = Employee("Amy", ["Skill"])
    employee2 = Employee("Beth", ["Skill"])
    constraint_verifier.verify_that(no_overlapping_shifts) \
        .given(employee1,
               Shift(1, DAY_START_TIME, DAY_END_TIME, "Location", "Skill", employee1),
               Shift(2, DAY_START_TIME, DAY_END_TIME, "Location 2", "Skill", employee1)) \
        .penalizes_by(int(timedelta(hours=8).total_seconds() // 60))

    constraint_verifier.verify_that(no_overlapping_shifts) \
        .given(employee1,
               Shift(1, DAY_START_TIME, DAY_END_TIME, "Location", "Skill", employee1),
               Shift(2, DAY_START_TIME, DAY_END_TIME, "Location 2", "Skill", employee2)) \
        .penalizes(0)

    constraint_verifier.verify_that(no_overlapping_shifts) \
        .given(employee1,
               Shift(1, DAY_START_TIME, DAY_END_TIME, "Location", "Skill", employee1),
               Shift(2, AFTERNOON_START_TIME, AFTERNOON_END_TIME, "Location 2", "Skill", employee1)) \
        .penalizes_by(int(timedelta(hours=4).total_seconds() // 60))


def test_one_shift_per_day():
    employee1 = Employee("Amy", ["Skill"])
    employee2 = Employee("Beth", ["Skill"])

    constraint_verifier.verify_that(no_overlapping_shifts) \
        .given(employee1,
               Shift(1, DAY_START_TIME, DAY_END_TIME, "Location", "Skill", employee1),
               Shift(2, DAY_START_TIME, DAY_END_TIME, "Location 2", "Skill", employee1)) \
        .penalizes(1)

    constraint_verifier.verify_that(no_overlapping_shifts) \
        .given(employee1,
               Shift(1, DAY_START_TIME, DAY_END_TIME, "Location", "Skill", employee1),
               Shift(2, DAY_START_TIME, DAY_END_TIME, "Location 2", "Skill", employee2)) \
        .penalizes(0)

    constraint_verifier.verify_that(no_overlapping_shifts) \
        .given(employee1,
               Shift(1, DAY_START_TIME, DAY_END_TIME, "Location", "Skill", employee1),
               Shift(2, AFTERNOON_START_TIME, AFTERNOON_END_TIME, "Location 2", "Skill", employee1)) \
        .penalizes(1)

    constraint_verifier.verify_that(no_overlapping_shifts) \
        .given(employee1,
               Shift(1, DAY_START_TIME, DAY_END_TIME, "Location", "Skill", employee1),
               Shift(2, DAY_START_TIME + timedelta(days=1), DAY_END_TIME + timedelta(days=1),
                     "Location 2", "Skill", employee1)) \
        .penalizes(0)


def test_at_least_10_hours_between_consecutive_shifts():
    employee1 = Employee("Amy", ["Skill"])
    employee2 = Employee("Beth", ["Skill"])
    constraint_verifier.verify_that(at_least_10_hours_between_two_shifts) \
        .given(employee1,
               Shift(1, DAY_START_TIME, DAY_END_TIME, "Location", "Skill", employee1),
               Shift(2, AFTERNOON_END_TIME, DAY_START_TIME + timedelta(days=1), "Location 2", "Skill", employee1)) \
        .penalizes_by(360)

    constraint_verifier.verify_that(at_least_10_hours_between_two_shifts) \
        .given(employee1,
               Shift(1, DAY_START_TIME, DAY_END_TIME, "Location", "Skill", employee1),
               Shift(2, DAY_END_TIME, DAY_START_TIME + timedelta(days=1), "Location 2", "Skill", employee1)) \
        .penalizes_by(600)

    constraint_verifier.verify_that(at_least_10_hours_between_two_shifts) \
        .given(employee1,
               Shift(1, DAY_START_TIME, DAY_END_TIME, "Location", "Skill", employee1),
               Shift(2, DAY_END_TIME + timedelta(hours=10), DAY_START_TIME + timedelta(days=1), "Location 2",
                     "Skill", employee1)) \
        .penalizes(0)

    constraint_verifier.verify_that(at_least_10_hours_between_two_shifts) \
        .given(employee1,
               Shift(1, DAY_START_TIME, DAY_END_TIME, "Location", "Skill", employee1),
               Shift(2, AFTERNOON_END_TIME, DAY_START_TIME + timedelta(days=1), "Location 2", "Skill", employee2)) \
        .penalizes(0)

    constraint_verifier.verify_that(at_least_10_hours_between_two_shifts) \
        .given(employee1,
               Shift(1, DAY_START_TIME, DAY_END_TIME, "Location", "Skill", employee1),
               Shift(2, DAY_START_TIME + timedelta(days=1), DAY_END_TIME + timedelta(days=1),
                     "Location 2", "Skill", employee1)) \
        .penalizes(0)


def test_unavailable_employee():
    employee1 = Employee("Amy", ["Skill"])
    employee2 = Employee("Beth", ["Skill"])
    unavailability = Availability(employee1, DAY_1, AvailabilityType.UNAVAILABLE)
    desired = Availability(employee1, DAY_1, AvailabilityType.DESIRED)
    constraint_verifier.verify_that(unavailable_employee) \
        .given(employee1,
               unavailability,
               Shift(1, DAY_START_TIME, DAY_END_TIME, "Location", "Skill", employee1)) \
        .penalizes_by(int(timedelta(hours=8).total_seconds() // 60))

    constraint_verifier.verify_that(unavailable_employee) \
        .given(employee1,
               unavailability,
               Shift(1, DAY_START_TIME + timedelta(days=1), DAY_END_TIME + timedelta(days=1),
                     "Location", "Skill", employee1)) \
        .penalizes(0)

    constraint_verifier.verify_that(unavailable_employee) \
        .given(employee1,
               unavailability,
               Shift(1, DAY_START_TIME, DAY_END_TIME, "Location", "Skill", employee2)) \
        .penalizes(0)

    constraint_verifier.verify_that(unavailable_employee) \
        .given(employee1,
               desired,
               Shift(1, DAY_START_TIME, DAY_END_TIME, "Location", "Skill", employee1)) \
        .penalizes(0)


def test_desired_day_for_employee():
    employee1 = Employee("Amy", ["Skill"])
    employee2 = Employee("Beth", ["Skill"])
    unavailability = Availability(employee1, DAY_1, AvailabilityType.UNAVAILABLE)
    desired = Availability(employee1, DAY_1, AvailabilityType.DESIRED)
    constraint_verifier.verify_that(desired_day_for_employee) \
        .given(employee1,
               desired,
               Shift(1, DAY_START_TIME, DAY_END_TIME, "Location", "Skill", employee1)) \
        .rewards_with(int(timedelta(hours=8).total_seconds() // 60))

    constraint_verifier.verify_that(desired_day_for_employee) \
        .given(employee1,
               desired,
               Shift(1, DAY_START_TIME + timedelta(days=1), DAY_END_TIME + timedelta(days=1),
                     "Location", "Skill", employee1)) \
        .rewards(0)

    constraint_verifier.verify_that(desired_day_for_employee) \
        .given(employee1,
               desired,
               Shift(1, DAY_START_TIME, DAY_END_TIME, "Location", "Skill", employee2)) \
        .rewards(0)

    constraint_verifier.verify_that(desired_day_for_employee) \
        .given(employee1,
               unavailability,
               Shift(1, DAY_START_TIME, DAY_END_TIME, "Location", "Skill", employee1)) \
        .rewards(0)


def test_undesired_day_for_employee():
    employee1 = Employee("Amy", ["Skill"])
    employee2 = Employee("Beth", ["Skill"])
    unavailability = Availability(employee1, DAY_1, AvailabilityType.UNAVAILABLE)
    undesired = Availability(employee1, DAY_1, AvailabilityType.UNDESIRED)
    constraint_verifier.verify_that(undesired_day_for_employee) \
        .given(employee1,
               undesired,
               Shift(1, DAY_START_TIME, DAY_END_TIME, "Location", "Skill", employee1)) \
        .penalizes_by(int(timedelta(hours=8).total_seconds() // 60))

    constraint_verifier.verify_that(undesired_day_for_employee) \
        .given(employee1,
               undesired,
               Shift(1, DAY_START_TIME + timedelta(days=1), DAY_END_TIME + timedelta(days=1),
                     "Location", "Skill", employee1)) \
        .penalizes(0)

    constraint_verifier.verify_that(undesired_day_for_employee) \
        .given(employee1,
               undesired,
               Shift(1, DAY_START_TIME, DAY_END_TIME, "Location", "Skill", employee2)) \
        .penalizes(0)

    constraint_verifier.verify_that(undesired_day_for_employee) \
        .given(employee1,
               unavailability,
               Shift(1, DAY_START_TIME, DAY_END_TIME, "Location", "Skill", employee1)) \
        .penalizes(0)
