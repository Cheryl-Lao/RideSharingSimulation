class Location:
    def __init__(self, row, column):
        """Initialize a location.

        @type self: Location
        @type row: int
        @type column: int
        @rtype: None
        """

        if row >= 0 and column >= 0:
            self.m = column
            self.n = row
        else:
            print("Please enter only positive coordinates")

    def __str__(self):
        """Return a string representation.

        @rtype: str

        >>> location1 = Location(5,2)
        >>> print (location1)
        "5 streets from the left, 2 streets up"
        """

        return "{} streets from the left, {} streets up".format(self.m, self.n)

    def __eq__(self, other):
        """Return True if self equals other, and false otherwise.

        @rtype: bool

        >>> location1 = Location(5,6)
        >>> location2 = Location(5,6)
        >>> location1 == location2
        True
        """

        return self.m == other.m and self.n == other.n


def manhattan_distance(origin, destination):
    """Return the Manhattan distance between the origin and the destination.

    @type origin: Location
    @type destination: Location
    @rtype: int

    >>> origin1 = Location(1,2)
    >>> destination1 = Location (2,3)
    >>> manhattan_distance(origin1,destination1)
    2
    """

    latitude = abs(destination.n - origin.n)
    longitude = abs(destination.m - origin.m)
    return longitude + latitude


def deserialize_location(location_str):
    """Deserialize a location.

    @type location_str: str
        A location in the format 'row,col'
    @rtype: Location

    >>> loc_str = "22,33"
    >>> deserialize_location(loc_str)
    "22 streets from the left, 33 streets up"
    """

    row = ""

    i = 0

    while location_str[i] != ",":
        row += location_str[i]
        i += 1
    row = int(row)
    column = int(location_str[i+1:])

    return Location(column, row)
