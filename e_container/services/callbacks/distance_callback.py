from e_container.services.data_service import DataService


class CreateDistanceCallback(object):
    """Create callback to calculate distances between points."""

    def __init__(self, locations, depot):
        """Initialize distance array."""
        self.matrix = {}

        for i, from_node in enumerate(locations):
            self.matrix[i] = {}
            for j, to_node in enumerate(locations):
                if from_node == depot or to_node == depot or i == j:
                    self.matrix[i][j] = 0
                else:
                    self.matrix[i][j] = DataService.calculate_distance(from_node, to_node)

    def distance(self, i, j):
        return self.matrix[i][j]
