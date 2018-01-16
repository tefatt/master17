from e_container.services.data_service import DataService


class CreateDistanceCallback(object):
    """Create callback to calculate distances between points."""

    def __init__(self, locations, depot):
        """Initialize distance array."""
        try:
            self.matrix = {}

            visited_pairs = list()
            for i, from_node in enumerate(locations):
                self.matrix[i] = {}
                for j, to_node in enumerate(locations):
                    if i == j:
                        self.matrix[i][j] = 0
                    else:
                        if (i, j) in visited_pairs:
                            self.matrix[i][j] = self.matrix[j][i]
                            continue
                        self.matrix[i][j] = DataService.calculate_distance(from_node, to_node)
                        visited_pairs.append((j, i))
        except Exception:
            X = 2

    def distance(self, i, j):
        return self.matrix[i][j]
