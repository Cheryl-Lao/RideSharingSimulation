from driver import Driver
from rider import Rider
from container import PriorityQueue

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
        # TODO

        #_waiting_list is a queue-like list.
        # The person at the lowest index has been waiting the longest
        #The person at the highest index has been waiting the shortest time
        self._waiting_list = []
        self._available_drivers = []


    def __str__(self):
        """Return a string representation.

        @type self: Dispatcher
        @rtype: str
        """

        # TODO
        return "Waiting List: {}  Available Drivers: {}".format(self._waiting_list, self._available_drivers)

    def request_driver(self, rider):
        """Return a driver for the rider, or None if no driver is available.

        Add the rider to the waiting list if there is no available driver.

        @type self: Dispatcher
        @type rider: Rider
        @rtype: Driver | None
        """

        # TODO

        #Store the indexes of all of the available drivers

        #Add the rider to the waiting list if there are no available drivers
        if len(self._available_drivers) == 0:
            self._waiting_list.append(rider)
            return None

        #Assign a suitable driver to the rider
        else:
            pickup_place = rider.location
            closest_driver = self._available_drivers[0]

            #finding the driver that will get there the fastest
            for driver in self._available_drivers:
                if (driver.get_travel_time(rider.destination)
                    < closest_driver.get_travel_time(rider.destination)):
                    closest_driver = driver

                    #assigning the rider to that driver
                    closest_driver.rider = rider

            return closest_driver


    def request_rider(self, driver):
        """Return a rider for the driver, or None if no rider is available.

        If this is a new driver, register the driver for future rider requests.

        @type self: Dispatcher
        @type driver: Driver
        @rtype: Rider | None
        """

        # TODO
        if driver not in self._available_drivers:
            self._available_drivers.append(driver)

        if len(self._waiting_list) > 0:
            assigned_rider = self._waiting_list.pop(0)
            self._available_drivers.remove(driver)
            return assigned_rider
        else:
            return None

    def cancel_ride(self, rider):
        """Cancel the ride for rider.

        @type self: Dispatcher
        @type rider: Rider
        @rtype: None
        """

        # TODO

        if rider in self._waiting_list:
            self._waiting_list.remove(rider)
