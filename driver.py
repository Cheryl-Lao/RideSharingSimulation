from location import Location, manhattan_distance
from rider import Rider


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

    def __init__(self, identifier, location, speed):
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
        #intended destination
        self.destination = None
        #status of the driver
        self.status = "idle"
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
        return self.speed * (manhattan_distance(self.location, destination))

    def start_drive(self, location):
        """Start driving to the location and return the time the drive will take.

        @type self: Driver
        @type location: Location
        @rtype: int
        """
        # TODO
        pass

    def end_drive(self):
        """End the drive and arrive at the destination.

        Precondition: self.destination is not None.

        @type self: Driver
        @rtype: None
        """
        # TODO
        pass

    def start_ride(self, rider):
        """Start a ride and return the time the ride will take.

        @type self: Driver
        @type rider: Rider
        @rtype: int
        """
        # TODO
        pass

    def end_ride(self):
        """End the current ride, and arrive at the rider's destination.

        Precondition: The driver has a rider.
        Precondition: self.destination is not None.

        @type self: Driver
        @rtype: None
        """
        # TODO
        pass
