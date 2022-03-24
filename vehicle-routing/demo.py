from random import Random

class DemoDataBuilder:
    def __init__(self, Location, Depot, Customer, Vehicle, VehicleRoutingSolution, calculator):
        self.southWestCorner = None
        self.northEastCorner = None
        self.customerCount = None
        self.vehicleCount = None
        self.depotCount = None
        self.minDemand = None
        self.maxDemand = None
        self.vehicleCapacity = None
        self.Location = Location
        self.Depot = Depot
        self.Customer = Customer
        self.Vehicle = Vehicle
        self.VehicleRoutingSolution = VehicleRoutingSolution
        self.distance_calculator = calculator

    @staticmethod
    def builder(Location, Depot, Customer, Vehicle, VehicleRoutingSolution, calculator):
        return DemoDataBuilder(Location, Depot, Customer, Vehicle, VehicleRoutingSolution, calculator)

    def set_south_west_corner(self, southWestCorner):
        self.southWestCorner = southWestCorner
        return self

    def set_north_east_corner(self, northEastCorner):
        self.northEastCorner = northEastCorner
        return self

    def set_min_demand(self, minDemand):
        self.minDemand = minDemand
        return self

    def set_max_demand(self, maxDemand):
        self.maxDemand = maxDemand
        return self

    def set_customer_count(self, customerCount):
        self.customerCount = customerCount
        return self

    def set_vehicle_count(self, vehicleCount):
        self.vehicleCount = vehicleCount
        return self

    def set_depot_count(self, depotCount):
        self.depotCount = depotCount
        return self

    def set_vehicle_capacity(self, vehicleCapacity):
        self.vehicleCapacity = vehicleCapacity
        return self

    def build(self):
        if self.minDemand < 1:
            raise ValueError("minDemand (" + self.minDemand + ") must be greater than zero.")
        if self.maxDemand < 1:
            raise ValueError("maxDemand (" + self.maxDemand + ") must be greater than zero.")
        if self.minDemand >= self.maxDemand:
            raise ValueError("maxDemand (" + self.maxDemand + ") must be greater than minDemand ("
                             + self.minDemand + ").")
        if self.vehicleCapacity < 1:
            raise ValueError("Number of vehicleCapacity (" + self.vehicleCapacity + ") must be greater than zero.")
        if self.customerCount < 1:
            raise ValueError("Number of customerCount (" + self.customerCount + ") must be greater than zero.")
        if self.vehicleCount < 1:
            raise ValueError("Number of vehicleCount (" + self.vehicleCount + ") must be greater than zero.")
        if self.depotCount < 1:
            raise ValueError("Number of depotCount (" + self.depotCount + ") must be greater than zero.")

        if self.northEastCorner.latitude <= self.southWestCorner.latitude:
            raise ValueError("northEastCorner.getLatitude (" + self.northEastCorner.latitude
               + ") must be greater than southWestCorner.getLatitude(" +  self.southWestCorner.latitude + ").")

        if self.northEastCorner.longitude <= self.southWestCorner.longitude:
            raise ValueError("northEastCorner.getLongitude (" + self.northEastCorner.longitude
               + ") must be greater than southWestCorner.getLongitude(" +  self.southWestCorner.longitude + ").")

        name = "demo"

        random = Random(0)
        id_sequence = [0]

        def generate_id():
            out = id_sequence[0]
            id_sequence[0] = out + 1
            return str(out)

        generate_latitude = lambda: random.uniform(self.southWestCorner.latitude, self.northEastCorner.latitude)
        generate_longitude = lambda: random.uniform(self.southWestCorner.longitude, self.northEastCorner.longitude)

        generate_demand = lambda: random.randint(self.minDemand, self.maxDemand)

        depot_list = []
        random_depot = lambda: random.choice(depot_list)

        generate_depot = lambda: self.Depot(
            generate_id(),
            self.Location(generate_latitude(), generate_longitude()))

        for i in range(self.depotCount):
            depot_list.append(generate_depot())

        generate_vehicle = lambda: self.Vehicle(
            generate_id(),
            self.vehicleCapacity,
            random_depot())

        vehicle_list = []
        for i in range(self.vehicleCount):
            vehicle_list.append(generate_vehicle())

        generate_customer = lambda: self.Customer(
            generate_id(),
            self.Location(generate_latitude(), generate_longitude()),
            generate_demand())

        customer_list = []
        for i in range(self.customerCount):
            customer_list.append(generate_customer())

        location_list = []
        for customer in customer_list:
            location_list.append(customer.location)
        for depot in depot_list:
            location_list.append(depot.location)

        self.distance_calculator.init_distance_maps(location_list)

        return self.VehicleRoutingSolution(name, location_list,
                                      depot_list, vehicle_list, customer_list, self.southWestCorner,
                                      self.northEastCorner)