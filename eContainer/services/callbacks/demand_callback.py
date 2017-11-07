class CreateDemandCallback(object):
    """Create callback to get demands at each location."""

    def __init__(self, demands):
        self.matrix = demands

    def demand(self, position):
        return self.matrix[position]
