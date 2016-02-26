"""
The rider module contains the Rider class. It also contains
constants that represent the status of the rider.

=== Constants ===
@type WAITING: str
    A constant used for the waiting rider status.
@type CANCELLED: str
    A constant used for the cancelled rider status.
@type SATISFIED: str
    A constant used for the satisfied rider status
"""

WAITING = "waiting"
CANCELLED = "cancelled"
SATISFIED = "satisfied"


class Rider:

    def __init__(self, identifier, origin, destination, patience):
        """
        Create a Rider object with id, origin and destination

        :param identifier:
            Unique identifier for the rider

        :type identifier: str

        :param origin:
            The location where the rider wants to be picked up

        :type origin: Location

        :param destination:
            The location to which the rider wishes to be driven

        :type destination: Location

        :param patience:
            The number of minutes the rider will wait before cancelling

        :type patience: int

        :rtype: None
        """

        self.id = identifier
        self.origin = origin
        self.destination = destination
        self.patience = patience
        # Set them to be waiting on default
        self.status = WAITING

    def __str__(self):
        """Return a string representation.
        @type self: Rider
        @rtype: str

        >>> name1 = 'Jane Doe'
        >>> origin1 = Location(10,13)
        >>> destination1 = Location(1,2)
        >>> patience1 = 20
        >>> rider = Rider(name1, origin1, destination1, patience1)
        >>> print(rider)
        >>> "Jane Does wants to go from 10 streets left, 13 up to 1 streets left, 2 up and is waiting."
        """

        return "{} wants to go from ({}) to ({}) and is {}"\
            .format(self.id, self.origin, self.destination, self.status)
