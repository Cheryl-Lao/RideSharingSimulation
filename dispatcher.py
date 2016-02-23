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

        self.waiting_list = PriorityQueue()
        self.available_drivers = []


    def __str__(self):
        """Return a string representation.

        @type self: Dispatcher
        @rtype: str
        """
        # TODO
        return "Waiting List: {}  Available Drivers: {}".format(self.waiting_list, self.available_drivers)

    def request_driver(self, rider):
        """Return a driver for the rider, or None if no driver is available.

        Add the rider to the waiting list if there is no available driver.

        @type self: Dispatcher
        @type rider: Rider
        @rtype: Driver | None
        """

        # TODO
        #Add the rider to the waiting list if there are no available drivers
        if len(self.available_drivers) == 0:
            self.waiting_list.append(rider)
            return None
        else:
            pickup_place = rider.location
            closest_driver = self.available_drivers[0]

            #finding the driver that will get there the fastest
            for driver in self.available_drivers:
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

        self.available_drivers.append(driver)# or do i add driver to a separate "driving fleet" list

        if len(self.waiting_list) > 0:
            assigned_rider = self.waiting_list.pop(0) #is the longest waiting rider the first one on the list?
            self.available_drivers.remove(driver)
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

        if rider in self.waiting_list:
            self.waiting_list.remove(rider)
