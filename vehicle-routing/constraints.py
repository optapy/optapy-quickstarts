from optapy import constraint_provider
from optapy.score import HardSoftScore
from optapy.constraint import ConstraintFactory
from domain import Vehicle


@constraint_provider
def vehicle_routing_constraints(constraint_factory: ConstraintFactory):
    return [
        vehicle_capacity(constraint_factory),
        total_distance(constraint_factory)
    ]


def vehicle_capacity(constraint_factory: ConstraintFactory):
    return constraint_factory.for_each(Vehicle) \
               .filter(lambda vehicle: vehicle.get_total_demand() > vehicle.capacity) \
               .penalize("vehicle_capacity", HardSoftScore.ONE_HARD,
                         lambda vehicle: vehicle.get_total_demand() - vehicle.capacity)


def total_distance(constraint_factory: ConstraintFactory):
    return constraint_factory.for_each(Vehicle) \
        .penalize("distance_from_previous_standstill", HardSoftScore.ONE_SOFT,
                  lambda vehicle: vehicle.get_total_distance_meters())
