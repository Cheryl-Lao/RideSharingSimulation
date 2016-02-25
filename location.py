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
        """
        return "{} streets from the left, {} streets up".format(self.m, self.n)

    def __eq__(self, other):
        """Return True if self equals other, and false otherwise.

        @rtype: bool
        """
        return self.m == other.m and self.n == other.n


def manhattan_distance(origin, destination):
    """Return the Manhattan distance between the origin and the destination.

    @type origin: Location
    @type destination: Location
    @rtype: int
    """

    latitude = abs(destination.n - origin.n)
    longitude = abs(destination.m - origin.m)
    return longitude + latitude


def deserialize_location(location_str):
    """Deserialize a location.

    @type location_str: str
        A location in the format 'row,col'
    @rtype: Location
    """

    row = ""

    i=0

    while location_str[i] != ",":
        row += location_str[i]
        i += 1
    row = int(row)
    column = int(location_str[i+1:])

    return Location(column, row)
