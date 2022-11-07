from domain import Location, Depot, Customer, Vehicle, VehicleRoutingSolution, EuclideanDistanceCalculator
from constraints import vehicle_routing_constraints, total_distance, vehicle_capacity

from optapy.test import ConstraintVerifier, constraint_verifier_build

constraint_verifier: ConstraintVerifier = constraint_verifier_build(vehicle_routing_constraints,
                                                                    VehicleRoutingSolution, Vehicle)
location1 = Location(1, 0.0, 0.0)
location2 = Location(2, 0.0, 4.0)
location3 = Location(3, 3.0, 0.0)

EuclideanDistanceCalculator().init_distance_maps((location1, location2, location3))


def test_vehicle_capacity_unpenalized():
    vehicle_a = Vehicle(1, 100, Depot(1, location1))
    customer_1 = Customer(2, location2, 80)
    vehicle_a.get_customer_list().append(customer_1)

    constraint_verifier.verify_that(vehicle_capacity) \
        .given(vehicle_a, customer_1) \
        .penalizes_by(0)


def test_vehicle_capacity_penalized():
    vehicle_a = Vehicle(1, 100, Depot(1, location1))
    customer_1 = Customer(2, location2, 80)
    vehicle_a.get_customer_list().append(customer_1)

    customer_2 = Customer(3, location3, 40)
    vehicle_a.get_customer_list().append(customer_2)

    constraint_verifier.verify_that(vehicle_capacity) \
        .given(vehicle_a, customer_1, customer_2) \
        .penalizes_by(20)


def test_total_distance():
    vehicle_a = Vehicle(1, 100, Depot(1, location1))
    customer_1 = Customer(2, location2, 80)
    vehicle_a.get_customer_list().append(customer_1)
    customer_2 = Customer(3, location3, 40)
    vehicle_a.get_customer_list().append(customer_2)

    constraint_verifier.verify_that(total_distance) \
        .given(vehicle_a, customer_1, customer_2) \
        .penalizes_by((4 + 5 + 3) * EuclideanDistanceCalculator.METERS_PER_DEGREE)
