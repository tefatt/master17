from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

from e_container.services.callbacks import distance_callback, demand_callback


class OptimizationService:
    def __init__(self, locations, vehicles, demands, depot):
        self.locations = [[float(loc.latitude), float(loc.longitude)] for loc in locations]
        self.vehicles = list(vehicles)
        self.demands = list(demands.values())
        self.depot = depot.location
        # location_ids = list(locations.values_list('id', flat=True)).insert(0, self.depot.id)
        routing = pywrapcp.RoutingModel(len(locations), len(vehicles), 0)
        search_parameters = pywrapcp.RoutingModel_DefaultSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        # Callback to the distance function.
        dist_between_locations = distance_callback.CreateDistanceCallback(self.locations, self.depot)
        self.dist_callback = dist_between_locations.distance
        routing.SetArcCostEvaluatorOfAllVehicles(self.dist_callback)

        # Put a callback to the demands.
        demands_at_locations = demand_callback.CreateDemandCallback(self.demands)
        self.demands_callback = demands_at_locations.demand

        # Add a dimension for demand.
        slack_max = 0
        vehicle_capacity = [int(v) for v in (vehicles.values_list('capacity', flat=True))]
        fix_start_cumul_to_zero = True
        demand = "Demand"
        routing.AddDimension(self.demands_callback, slack_max, min(vehicle_capacity),
                             fix_start_cumul_to_zero, demand)
        self.routing = routing
        self.assignment = routing.SolveWithParameters(search_parameters)

    def optimize(self):
        solution = dict()
        if self.assignment:
            for vehicle_nbr in range(len(self.vehicles)):
                index = self.routing.Start(vehicle_nbr)
                index_next = self.assignment.Value(self.routing.NextVar(index))
                route = list()
                route_dist = 0
                route_demand = 0

                while not self.routing.IsEnd(index_next):
                    node_index = self.routing.IndexToNode(index)
                    node_index_next = self.routing.IndexToNode(index_next)
                    if node_index != self.depot:
                        route.extend(node_index)
                        # Add the distance to the next node.
                        route_dist += self.dist_callback(node_index, node_index_next)
                        # Add demand.
                        route_demand += self.demands[node_index_next]
                        index = index_next
                        index_next = self.assignment.Value(self.routing.NextVar(index))

                node_index = self.routing.IndexToNode(index)
                node_index_next = self.routing.IndexToNode(index_next)
                route.extend(node_index)
                route_dist += self.dist_callback(node_index, node_index_next)

                solution[route] = (route_demand, route_dist)
        return solution
