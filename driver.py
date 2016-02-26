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

        self.id = identifier
        self.location = location
        self.speed = speed
        # Idle on default
        self.is_idle = True
        # The person that the driver is carrying
        self.rider = None
        self.destination = None

    def __str__(self):
        """Return a string representation.

        @type self: Driver
        @rtype: str

        >>> location1 = Location(3,4)
        >>> speed1 = 3
        >>> id1 = 'John Doe'
        >>> driver1 = Driver(id1, location1, speed1)
        >>> print(driver1)
        "John Doe at 3 streets from the left, 4 streets up has a speed of 3 and
        is idle"
        """

        if self.is_idle:
            idle = "is idle"
        else:
            idle = "is driving"

        return "{} at {} has a speed of {} and {}".format(
            self.id, self.location.__str__(), self.speed, idle)

    def __eq__(self, other):
        """Return True if self equals other, and false otherwise.

        @type self: Driver
        @rtype: bool

        >>> location1 = Location(1,2)
        >>> speed1 = 3
        >>> id1 = 'John Doe'
        >>> driver1 = Driver(id1, location1, speed1)
        >>> location2 = Location(1,2)
        >>> speed2 = 3
        >>> id2 = 'John Doe'
        >>> driver2 = Driver(id2, location2, speed2)
        >>> driver1 == driver2
        True
        """

        return self.id == other.id and self.speed == other.speed \
            and self.location == other.location

    def get_travel_time(self, destination):
        """Return the time it will take to arrive at the destination,
        rounded to the nearest integer.

        @type self: Driver
        @type destination: Location
        @rtype: int

        >>> location1 = Location(1,2)
        >>> speed1 = 3
        >>> id1 = 'John Doe'
        >>> driver = Driver(id1, location1, speed1)
        >>> destination1 = Location (2,4)
        >>> driver.get_travel_time(destination1)
        1
        """

        return int(round((manhattan_distance(self.location, destination)) /
                   self.speed, 0))

    def start_drive(self, location):
        """"Start driving to the location and return the time the drive will take.

        @type self: Driver
        @type location: Location
        @rtype: int

        >>> location1 = Location(1,2)
        >>> speed1 = 3
        >>> id1 = 'John Doe'
        >>> driver = Driver(id1, location1, speed1)
        >>> location2 = Location (2,4)
        >>> driver.start_drive(location2)
        1

        """

        self.destination = location
        self.is_idle = False
        return self.get_travel_time(location)

    def end_drive(self):
        """End the drive and arrive at the destination.

        Precondition: self.destination is not None.

        @type self: Driver
        @rtype: None

        >>> location1 = Location(1,2)
        >>> speed1 = 5
        >>> id1 = 'John Doe'
        >>> driver = Driver(id1, location1, speed1)
        >>> location2 = Location (2,4)
        >>> driver.start_drive(location2)
        1
        >>> driver.end_drive()
        >>> driver.destination
        None
        """

        self.location = self.destination
        self.is_idle = True
        self.destination = None

    def start_ride(self, rider):
        """Start a ride and return the time the ride will take.

        @type self: Driver
        @type rider: Rider
        @rtype: int

        >>> name1 = 'Jane Doe'
        >>> origin1 = Location(10,13)
        >>> destination1 = Location(1,2)
        >>> patience1 = 20
        >>> rider1 = Rider(name1, origin1, destination1, patience1)
        >>> speed2 = 4
        >>> id2 = 'John Doe'
        >>> driver = Driver(id2, origin1, speed2)
        >>> driver.start_ride(rider1)
        5
        """

        # Assign rider to the driver
        self.rider = rider
        # Goes towards the same dropoff location
        self.destination = rider.destination
        self.is_idle = False
        return self.get_travel_time(rider.destination)

    def end_ride(self):
        """End the current ride, and arrive at the rider's destination.

        Precondition: The driver has a rider.
        Precondition: self.destination is not None.

        @type self: Driver
        @rtype: None

        >>> name1 = 'Jane Doe'
        >>> origin1 = Location(10,13)
        >>> destination1 = Location(1,2)
        >>> patience1 = 20
        >>> rider1 = Rider(name1, origin1, destination1, patience1)
        >>> speed2 = 4
        >>> id2 = 'John Doe'
        >>> driver = Driver(id2, origin1, speed2)
        >>> driver.start_ride(rider1)
        5
        >>> driver.end_ride()
        >>> driver.destination
        None
        """
        print(str(self.location)+"CHECK 11")
        print(self.destination is None)
        if self.destination is not None:
            self.location = self.destination
        print(str(self.location)+"CHECK 12")
        self.is_idle = True
        self.destination = None
        self.rider = None
