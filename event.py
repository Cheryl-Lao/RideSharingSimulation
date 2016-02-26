"""Simulation Events

This file should contain all of the classes necessary to model the different
kinds of events in the simulation.
"""
from rider import Rider, WAITING, CANCELLED, SATISFIED
from dispatcher import Dispatcher
from driver import Driver
from location import deserialize_location
from monitor import Monitor, RIDER, DRIVER, REQUEST, CANCEL, PICKUP, DROPOFF


class Event:
    """An event.

    Events have an ordering that is based on the event timestamp: Events with
    older timestamps are less than those with newer timestamps.

    This class is abstract; subclasses must implement do().

    You may, if you wish, change the API of this class to add
    extra public methods or attributes. Make sure that anything
    you add makes sense for ALL events, and not just a particular
    event type.

    Document any such changes carefully!

    === Attributes ===
    @type timestamp: int
        A timestamp for this event.
    """

    def __init__(self, timestamp):
        """Initialize an Event with a given timestamp.

        @type self: Event
        @type timestamp: int
            A timestamp for this event.
            Precondition: must be a non-negative integer.
        @rtype: None

        >>> Event(7).timestamp
        7
        """

        self.timestamp = timestamp

    # The following six 'magic methods' are overridden to allow for easy
    # comparison of Event instances. All comparisons simply perform the
    # same comparison on the 'timestamp' attribute of the two events.

    def __eq__(self, other):
        """Return True iff this Event is equal to <other>.

        Two events are equal iff they have the same timestamp.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first == second
        False
        >>> second.timestamp = first.timestamp
        >>> first == second
        True
        """

        return self.timestamp == other.timestamp

    def __ne__(self, other):
        """Return True iff this Event is not equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first != second
        True
        >>> second.timestamp = first.timestamp
        >>> first != second
        False
        """
        return not self == other

    def __lt__(self, other):
        """Return True iff this Event is less than <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first < second
        True
        >>> second < first
        False
        """
        return self.timestamp < other.timestamp

    def __le__(self, other):
        """Return True iff this Event is less than or equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first <= first
        True
        >>> first <= second
        True
        >>> second <= first
        False
        """
        return self.timestamp <= other.timestamp

    def __gt__(self, other):
        """Return True iff this Event is greater than <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first > second
        False
        >>> second > first
        True
        """
        return not self <= other

    def __ge__(self, other):
        """Return True iff this Event is greater than or equal to <other>.

        @type self: Event
        @type other: Event
        @rtype: bool

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first >= first
        True
        >>> first >= second
        False
        >>> second >= first
        True
        """
        return not self < other

    def __str__(self):
        """Return a string representation of this event.

        @type self: Event
        @rtype: str
        """
        raise NotImplementedError("Implemented in a subclass")

    def do(self, dispatcher, monitor):
        """Do this Event.

        Update the state of the simulation, using the dispatcher, and any
        attributes according to the meaning of the event.

        Notify the monitor of any activities that have occurred during the
        event.

        Return a list of new events spawned by this event (making sure the
        timestamps are correct).

        Note: the "business logic" of what actually happens should not be
        handled in any Event classes.

        @type self: Event
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """
        raise NotImplementedError("Implemented in a subclass")


class RiderRequest(Event):
    """A rider requests a driver.

    === Attributes ===
    @type rider: Rider
        The rider.
    """

    def __init__(self, timestamp, rider):
        """Initialize a RiderRequest event.

        @type self: RiderRequest
        @type rider: Rider
        @rtype: None
        """
        super().__init__(timestamp)
        self.rider = rider

    def do(self, dispatcher, monitor):
        """Assign the rider to a driver or add the rider to a waiting list.
        If the rider is assigned to a driver, the driver starts driving to
        the rider.

        Return a Cancellation event. If the rider is assigned to a driver,
        also return a Pickup event.

        @type self: RiderRequest
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """

        monitor.notify(self.timestamp, RIDER, REQUEST,
                       self.rider.id, self.rider.origin)

        events = []
        driver = dispatcher.request_driver(self.rider)

        if driver is not None:
            travel_time = driver.start_drive(self.rider.origin)
            events.append(Pickup(self.timestamp + travel_time,
                                 self.rider, driver))
        events.append(Cancellation(self.timestamp + self.rider.patience,
                                   self.rider))

        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: RiderRequest
        @rtype: str
        """
        return "{} -- {}: Request a driver".format(self.timestamp, self.rider)


class DriverRequest(Event):
    """A driver requests a rider.

    === Attributes ===
    @type driver: Driver
        The driver.
    """

    def __init__(self, timestamp, driver):
        """Initialize a DriverRequest event.

        @type self: DriverRequest
        @type driver: Driver
        @rtype: None
        """
        super().__init__(timestamp)
        self.driver = driver

    def do(self, dispatcher, monitor):
        """Register the driver, if this is the first request, and
        assign a rider to the driver, if one is available.

        If a rider is available, return a Pickup event.

        @type self: DriverRequest
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]
        """
        # Notify the monitor about the request.

        # Request a rider from the dispatcher.
        # If there is one available, the driver starts driving towards the
        # rider, and the method returns a Pickup event for when the driver
        # arrives at the riders location.
        print(self.driver.location)
        monitor.notify(self.timestamp, DRIVER, REQUEST,
                       self.driver.id, self.driver.location)

        events = []

        # Find the the nearest rider
        rider = dispatcher.request_rider(self.driver)

        # If there was no rider, just return an empty list of events
        if rider is None:
            return events

        # Find how long it will take the the driver to reach the location
        travel_time = self.driver.get_travel_time(self.driver.destination)

        # Driver starts driving towards the rider's location
        self.driver.start_drive(self.driver.destination)

        # The poor driver is going to go there no matter what
        events.append(Pickup(self.timestamp + travel_time, rider, self.driver))

        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: DriverRequest
        @rtype: str
        """

        return "{} -- {}: Request a rider".format(self.timestamp, self.driver)


class Cancellation(Event):

    """Assign the rider to a driver or add the rider to a waiting list.
        If the rider is assigned to a driver, the driver starts driving to
        the rider.

        Change a waiting rider to a cancelled rider unless if the rider has
         already been picked up.

        @type self: Cancellation
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]

        >>> name1 = 'Jane Doe'
        >>> origin1 = Location(10,13)
        >>> destination1 = Location(1,2)
        >>> patience1 = 20
        >>> rider1 = Rider(name1, origin1, destination1, patience1)
        >>> location1 = Location(3,2)
        >>> speed1 = 5
        >>> id1 = 'John Doe'
        >>> driver1 = Driver(id1, location1, speed1)
        >>> dispatcher = Dispatcher()
        >>> dispatcher._available_drivers.append(driver1)
        >>> timestamp1 = 4
        >>> event1 = DriverRequest(timestamp1, driver1)
        >>> timestamp2 = event1.timestamp + rider1.patience
        >>> event2 = Cancellation(timestamp2,rider1)
        >>> rider1.status
        cancelled
        """

    def __init__(self, timestamp, rider):
        """Initialize a RiderRequest event.

        @type self: RiderRequest
        @type rider: Rider
        @rtype: None
        """
        super().__init__(timestamp)
        self.rider = rider

    def do(self, dispatcher, monitor):
        """Assign the rider to a driver or add the rider to a waiting list.
        If the rider is assigned to a driver, the driver starts driving to
        the rider.

        Change a waiting rider to a cancelled rider unless if the rider has
         already been picked up.

        @type self: Cancellation
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]

        >>> name1 = 'Jane Doe'
        >>> origin1 = Location(10,13)
        >>> destination1 = Location(1,2)
        >>> patience1 = 20
        >>> rider1 = Rider(name1, origin1, destination1, patience1)
        >>> location1 = Location(3,2)
        >>> speed1 = 5
        >>> id1 = 'John Doe'
        >>> driver1 = Driver(id1, location1, speed1)
        >>> dispatcher = Dispatcher()
        >>> dispatcher._available_drivers.append(driver1)
        >>> timestamp1 = 4
        >>> event1 = DriverRequest(timestamp1, driver1)
        >>> timestamp2 = event1.timestamp + rider1.patience
        >>> event2 = Cancellation(timestamp2,rider1)
        >>> rider1.status
        "cancelled"
        """

        events = []

        if self.rider.status == WAITING:

            self.rider.status = CANCELLED

            dispatcher.cancel_ride(self.rider)

            monitor.notify(self.timestamp, RIDER,
                           CANCEL, self.rider.id, self.rider.origin)

        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: Cancellation
        @rtype: str

        >>> name1 = 'Jane Doe'
        >>> origin1 = Location(10,13)
        >>> destination1 = Location(1,2)
        >>> patience1 = 20
        >>> rider1 = Rider(name1, origin1, destination1, patience1)
        >>> location1 = Location(3,2)
        >>> speed1 = 5
        >>> id1 = 'John Doe'
        >>> driver1 = Driver(id1, location1, speed1)
        >>> dispatcher = Dispatcher()
        >>> dispatcher._available_drivers.append(driver)
        >>> timestamp1 = 4
        >>> event1 = DriverRequest(timestamp1, driver1)
        >>> event2 = Cancellation(event1.timestamp,rider1)
        >>> print(event2)
        "4 -- Jane Doe: Cancel a ride"
        """

        return "{} -- {}: Cancel a ride"\
            .format(self.timestamp, self.rider.id)


class Pickup(Event):

    """
    Driver arrives at the location and picks up the rider if the rider has not
    cancelled, making the rider satisfied. A Dropoff event is scheduled at
    the estimated arrival time.

    If the rider has cancelled, the driver requests a new rider immediately

    @type self: Pickup
    @rtype: None

    """

    def __init__(self, timestamp, rider, driver):
        """Initialize a Pickup event.

        @type self: Pickup
        @type driver: Driver
        @type rider: Rider
        @rtype: None
        """
        super().__init__(timestamp)
        self.driver = driver
        self.rider = rider

    def do(self, dispatcher, monitor):

        """Assign the rider to a driver or add the rider to a waiting list.
        If the rider is assigned to a driver, the driver starts driving to
        the rider.

        Return a Cancellation event. If the rider is assigned to a driver,
        also return a Pickup event.

        @type self: RiderRequest
        @type dispatcher: Dispatcher
        @type monitor: Monitor
        @rtype: list[Event]

        >>> name1 = 'Jane Doe'
        >>> origin1 = Location(10,13)
        >>> destination1 = Location(1,2)
        >>> patience1 = 20
        >>> rider1 = Rider(name1, origin1, destination1, patience1)
        >>> location1 = Location(3,2)
        >>> speed1 = 5
        >>> id1 = 'John Doe'
        >>> driver1 = Driver(id1, location1, speed1)
        >>> dispatcher = Dispatcher()
        >>> dispatcher._available_drivers.append(driver)
        >>> timestamp1 = 4
        >>> event1 = DriverRequest(timestamp1, driver1)
        >>> timestamp2 = event1.timestamp + driver1.get_travel_time(rider1.origin)
        >>> event2 = Pickup(timestamp2, rider1, driver1)
        >>> rider1.status
        "satisfied"
        """

        monitor.notify(self.timestamp, DRIVER, PICKUP,
                       self.driver.id, self.driver.location)

        monitor.notify(self.timestamp, RIDER, PICKUP,
                       self.rider.id, self.rider.origin)

        events = []

        # The driver arrives
        self.driver.location = self.driver.destination
        print(str(self.driver.location) + "CHECK 1")
        # If the rider has cancelled, get a new rider
        if self.rider.status == CANCELLED:
            print("CHECK 4")
            if len(dispatcher._waiting_list) == 0:
                print(str(self.driver.location))
                print("CHECK 3")
                print("This new rider is none!!!")

            else:
                print(str(self.driver.location))
                print("CHECK 2")
                new_rider = dispatcher.request_rider(self.driver)
            events.append(DriverRequest(self.timestamp, self.driver))
        else:
            print(self.driver.location)
            print("CHECK 5")
            self.rider.status = SATISFIED
            travel_time = self.driver.start_ride(self.rider)
            print(str(self.driver.location)+"CHECK 6")
            events.append(Dropoff(self.timestamp + travel_time, self.rider,
                                  self.driver))
            print(str(self.driver.location)+"CHECK 7")

        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: Pickup
        @rtype: str

        >>> name1 = 'Jane Doe'
        >>> origin1 = Location(3,7)
        >>> destination1 = Location(1,2)
        >>> patience1 = 20
        >>> rider1 = Rider(name1, origin1, destination1, patience1)
        >>> location1 = Location(3,2)
        >>> speed1 = 5
        >>> id1 = 'John Doe'
        >>> driver1 = Driver(id1, location1, speed1)
        >>> dispatcher = Dispatcher()
        >>> dispatcher._available_drivers.append(driver)
        >>> timestamp1 = 4
        >>> event1 = DriverRequest(timestamp1, driver1)
        >>> timestamp2 = event1.timestamp + driver1.get_travel_time(rider1.origin)
        >>> event2 = Pickup(timestamp2, rider1, driver1)
        >>> print(event2)
        "5 -- John Doe at 3 streets from the left, 7 up has a speed of 5 and is idle: Pick up"
        """

        return "{} -- {}: Pick up".format(self.timestamp, self.driver)


class Dropoff(Event):

    """
    Driver arrives at the dropoff location to drop off the rider. The rider is
    left satisfied. The driver requests a new rider immediately.

    @type self: Dropoff
    @rtype: RiderRequest

    """

    def __init__(self, timestamp, rider, driver):
        """Initialize a Dropoff event.

        @type self: Dropoff
        @type driver: Driver
        @type rider: Rider
        @rtype: None
        """

        super().__init__(timestamp)
        self.driver = driver
        self.rider = rider

    def do(self, dispatcher, monitor):

        """Return a string representation of this event.

        @type self: Pickup
        @rtype: str

        >>> name1 = 'Jane Doe'
        >>> origin1 = Location(3,7)
        >>> destination1 = Location(1,2)
        >>> patience1 = 20
        >>> rider1 = Rider(name1, origin1, destination1, patience1)
        >>> location1 = Location(3,2)
        >>> speed1 = 5
        >>> id1 = 'John Doe'
        >>> driver1 = Driver(id1, location1, speed1)
        >>> dispatcher = Dispatcher()
        >>> dispatcher._available_drivers.append(driver1)
        >>> timestamp1 = 4
        >>> event1 = DriverRequest(timestamp1, driver1)
        >>> timestamp2 = event1.timestamp + driver1.get_travel_time(rider1.origin)
        >>> event2 = Pickup(timestamp2, rider1, driver1)
        >>> timestamp3 = event2.timestamp + event2.driver.get_travel_time(event2.rider.destination)
        >>> event3 = Dropoff(timestamp3, event2.rider, event2.driver)
        >>> print(event3)
        "6 -- John Doe at 1 streets from the left, 2 up has a speed of 5 and is idle: Pick up"
        """
        print(str(self.driver.location)+"CHECK 8")
        monitor.notify(self.timestamp, DRIVER, DROPOFF,
                       self.driver.id, self.driver.location)

        monitor.notify(self.timestamp, RIDER, DROPOFF,
                       self.rider.id, self.rider.destination)
        events = []

        """
        Sets the driver's location to the rider's destination
        Leaves the rider satisfied
        DriverRequest happens immediately after
        """

        self.rider.status = SATISFIED
        print(str(self.driver.location)+"CHECK 9")
        self.driver.end_ride()
        print(str(self.driver.location)+"CHECK 10")

        dispatcher.request_rider(self.driver)

        events.append(DriverRequest(self.timestamp, self.driver))

        return events

    def __str__(self):
        """Return a string representation of this event.

        @type self: Pickup
        @rtype: str
        """
        return "{} -- {}: Pick up".format(self.timestamp, self.driver)


def create_event_list(filename):
    """Return a list of Events based on raw list of events in <filename>.

    Precondition: the file stored at <filename> is in the format specified
    by the assignment handout.

    @param filename: str
        The name of a file that contains the list of events.
    @rtype: list[Event]
    """

    events = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                # Skip lines that are blank or start with #.
                continue

            # Create a list of words in the line, e.g.
            # ['10', 'RiderRequest', 'Cerise', '4,2', '1,5', '15'].
            # Note that these are strings, and you'll need to convert some
            # of them to a different type.
            tokens = line.split()
            timestamp = int(tokens[0])
            event_type = tokens[1]

            # HINT: Use Location.deserialize to convert the location string to
            # a location.
            event = None
            if event_type == "DriverRequest":

                # Create a DriverRequest event.
                event = DriverRequest(timestamp, Driver(tokens[2],
                                      deserialize_location(tokens[3]),
                                                        int(tokens[4])))

            elif event_type == "RiderRequest":

                # Create a RiderRequest event.
                event = RiderRequest(timestamp, Rider(tokens[2],
                                     deserialize_location(tokens[3]),
                                     deserialize_location(tokens[4]),
                                                      int(tokens[5])))
            events.append(event)

    return events
