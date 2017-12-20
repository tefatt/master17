from e_container.services.input_data_service import InputDataService


class CreateDistanceCallback(object):
    """Create callback to calculate distances between points."""

    def __init__(self, locations, depot):
        """Initialize distance array."""
        size = len(locations)
        self.matrix = {}

        for from_node in xrange(size):
            self.matrix[from_node] = {}
            for to_node in xrange(size):
                if from_node == depot or to_node == depot:
                    self.matrix[from_node][to_node] = 0
                else:
                    first_loc = locations[from_node]
                    second_loc = locations[to_node]
                    self.matrix[from_node][to_node] = InputDataService.calculate_distance(
                        first_loc, second_loc)

    def distance(self, from_node, to_node):
        return self.matrix[from_node][to_node]
