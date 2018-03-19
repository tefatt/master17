from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

from e_container.services.callbacks import distance_callback, demand_callback
from e_container.services.data_service import DataService
from e_container.utils.common_utils import CommonUtils
from e_container.models.recent_data import RecentDataModel


class OptimizationService:
    def __init__(self, locations, vehicles, demands, depot, start_location):
        self.depot = (depot.location.latitude, depot.location.longitude)
        self.depot_id = depot.location.id
        self.location_ids = [self.depot_id] + list(locations.values_list('id', flat=True))
        self.locations = [self.depot] + DataService.extract_lat_lon(locations)
        self.vehicles = list(vehicles)
        self.demands = [0] + list(demands.values())

        start_locations = DataService.define_start_locations(vehicles, self.location_ids, start_location)
        end_locations = [0] * len(vehicles)

        routing = pywrapcp.RoutingModel(locations.count() + 1, vehicles.count(), start_locations, end_locations)

        # define search parameters
        search_parameters = pywrapcp.RoutingModel_DefaultSearchParameters()
        search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.LOCAL_CHEAPEST_ARC
        search_parameters.time_limit_ms = 4 * 60 * 1000  # 4min
        search_parameters.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.TABU_SEARCH)
        routing.CloseModelWithParameters(search_parameters)

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

        # loads recent routes and takes them in consideration when generating new
        initial_routes = [CommonUtils.eval_type(v.last_save.route) for v in vehicles if
                          hasattr(v, 'last_save') and v.last_save.route]
        if len(initial_routes) == len(vehicles):
            initial_assignment = routing.ReadAssignmentFromRoutes(initial_routes, True)
            self.assignment = routing.SolveFromAssignmentWithParameters(initial_assignment, search_parameters)
        else:
            self.assignment = routing.SolveWithParameters(search_parameters)

    def optimize(self):
        solution = dict()
        if self.assignment:
            for vehicle_nbr, vehicle in enumerate(self.vehicles):
                index = self.routing.Start(vehicle_nbr)
                index_next = self.assignment.Value(self.routing.NextVar(index))
                route = list()
                route_distance = 0
                route_demand = 0

                while not self.routing.IsEnd(index_next):
                    node_index = self.routing.IndexToNode(index)
                    node_index_next = self.routing.IndexToNode(index_next)
                    route.append(self.location_ids[node_index])
                    # Add the distance to the next node.
                    route_distance += self.dist_callback(node_index, node_index_next)
                    # Add demand.
                    route_demand += self.demands[node_index_next]
                    index = index_next
                    index_next = self.assignment.Value(self.routing.NextVar(index))

                node_index = self.routing.IndexToNode(index)
                node_index_next = self.routing.IndexToNode(index_next)
                route.append(self.location_ids[node_index])
                route.append(self.location_ids[node_index_next])
                route_distance += self.dist_callback(node_index, node_index_next)

                solution[vehicle.id] = {'route': route, 'demand': route_demand, 'distance': route_distance}

                RecentDataModel.objects.update_or_create(vehicle=vehicle, defaults={'route': str(route),
                                                                                    'demand': route_demand,
                                                                                    'distance': route_distance})

        return solution
