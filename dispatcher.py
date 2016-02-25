from driver import Driver
from rider import Rider
from location import Location


class Dispatcher:
    """A dispatcher fulfills requests from riders and drivers for a
    ride-sharing service.

    When a rider requests a driver, the dispatcher assigns a driver to the
    rider. If no driver is available, the rider is placed on a waiting
    list for the next available driver. A rider that has not yet been
    picked up by a driver may cancel their request.

    When a driver requests a rider, the dispatcher assigns a rider from
    the waiting list to the driver. If there is no rider on the waiting list
    the dispatcher does nothing. Once a driver requests a rider, the driver
    is registered with the dispatcher, and will be used to fulfill future
    rider requests.
    """

    def __init__(self):
        """Initialize a Dispatcher.

        @type self: Dispatcher
        @rtype: None
        """

        # _waiting_list is a queue-like list.
        # The person at the lowest index has been waiting the longest
        # The person at the highest index has been waiting the shortest time
        self._waiting_list = []
        self._available_drivers = []

    def __str__(self):
        """Return a string representation.

        @type self: Dispatcher
        @rtype: str
        """

        str_waiting_list = []
        for rider in self._waiting_list:
            str_waiting_list.append(str(rider))

        str_available_drivers = []
        for driver in self._waiting_list:
            str_available_drivers.append(str(driver))

        return "Waiting List: {}  Available Drivers: {}".\
            format(str_waiting_list, str_available_drivers)

    def request_driver(self, rider):
        """Return a driver for the rider, or None if no driver is available.

        Add the rider to the waiting list if there is no available driver.

        @type self: Dispatcher
        @type rider: Rider
        @rtype: Driver | None
        """

        # Check whether or not there are available drivers
        i = 0

        nobody_available = True

        while i < len(self._available_drivers) and nobody_available:
            if self._available_drivers[i].is_idle:
                nobody_available = False
            i += 1

        # Add the rider to the waiting list if there are no available drivers
        if nobody_available:

            self._waiting_list.append(rider)
            return None

        # Assign a suitable driver to the rider
        else:
            pickup_place = rider.origin

            # Arbitrarily set the closest driver as the first one in
            # then list then compares to find the real closest one
            fastest_driver = self._available_drivers[0]

            # Finding the available driver that will get there the fastest
            # If two of them would get there the same time, take the
            # driver that comes earlier in the list
            for driver in self._available_drivers:
                if driver.get_travel_time(pickup_place) < \
                        fastest_driver.get_travel_time(pickup_place) \
                        and driver.is_idle:

                    fastest_driver = driver

            # assigning the rider to the fastest driver
            fastest_driver.rider = rider

            return fastest_driver

    def request_rider(self, driver):
        """Return a rider for the driver, or None if no rider is available.

        If this is a new driver, register the driver for future rider requests.

        @type self: Dispatcher
        @type driver: Driver
        @rtype: Rider | None
        """

        if driver not in self._available_drivers:
            self._available_drivers.append(driver)

        if len(self._waiting_list) == 0:
            return None

        else:
            # The rider at the front of the list has been waiting the longest
            assigned_rider = self._waiting_list.pop(0)
            # Driver starts going towards the rider
            driver.destination = assigned_rider.origin

        return assigned_rider

    def cancel_ride(self, rider):
        """Cancel the ride for rider.

        @type self: Dispatcher
        @type rider: Rider
        @rtype: None

        >>> name1 = 'Jane Doe'
        >>> origin1 = Location(12,13)
        >>> destination1 = Location(1,2)
        >>> patience1 = 20
        >>> rider1 = Rider(name1, origin1, destination1, patience1)
        >>> dispatcher = Dispatcher()
        >>> dispatcher._waiting_list.append(rider1)
        >>> dispatcher.cancel_ride(rider1)
        >>> dispatcher._waiting_list
        []
        """

        self._waiting_list.remove(rider)

