from location import Location, manhattan_distance
from rider import Rider

IDLE = "idle"
DRIVING = "driving"

class Driver:
    """A driver for a ride-sharing service.

    === Attributes ===
    @type id: str
        A unique identifier for the driver.
    @type location: Location
        The current location of the driver.
    @type is_idle: bool
        A property that is True if the driver is idle and False otherwise.
    """

    def __init__(self, identifier, location, speed, destination = None):
        """Initialize a Driver.

        @type self: Driver
        @type identifier: str
        @type location: Location
        @type speed: int
        @rtype: None
        """

        self.name = identifier
        self.location = location
        self.speed = speed
        #status of the driver
        self.status = "Idle"
        #the person that the driver is carrying
        self.rider = None

    def __str__(self):
        """Return a string representation.

        @type self: Driver
        @rtype: str
        """
        return "{} at {} is driving at a speed of {}".format (\
            self.name, self.location.__str__(), self.speed)

    def __eq__(self, other):
        """Return True if self equals other, and false otherwise.

        @type self: Driver
        @rtype: bool
        """
        return self.name == other.name and self.speed == other.speed \
                and self.location ==other.location

    def get_travel_time(self, destination):
        """Return the time it will take to arrive at the destination,
        rounded to the nearest integer.

        @type self: Driver
        @type destination: Location
        @rtype: int
        """
        return round((manhattan_distance(self.location, destination)) / self.speed, 2)

    def start_drive(self, location):
        """Start driving to the location and return the time the drive will take.

        @type self: Driver
        @type location: Location
        @rtype: int
        """
        # TODO

        self.status = DRIVING #Do I need to remove it from the available drivers??
        self.destination = location
        return self.get_travel_time(location)

    def end_drive(self):
        """End the drive and arrive at the destination.

        Precondition: self.destination is not None.

        @type self: Driver
        @rtype: None
        """
        # TODO

        self.status = IDLE
        self.location = self.destination
        self.destination = None


    def start_ride(self, rider):
        """Start a ride and return the time the ride will take.

        @type self: Driver
        @type rider: Rider
        @rtype: int
        """
        # TODO

        #assign rider to the driver
        self.rider = rider
        self.status = DRIVING
        self.destination = rider.destination

        return self.get_travel_time(rider.destination)

    def end_ride(self):
        """End the current ride, and arrive at the rider's destination.

        Precondition: The driver has a rider.
        Precondition: self.destination is not None.

        @type self: Driver
        @rtype: None
        """
        # TODO

        self.status = IDLE
        self.location = self.destination
        self.rider = None
        #Do I need to change the rider's status to satisfied??
