from celery import task
from celery import chord, group

from e_container.services.pubsub_service import PubSubService
from e_container.services.data_service import DataService
from e_container.services.optimization_service import OptimizationService
from e_container.models.municipality import MunicipalityModel
from e_container.models.depot import DepotModel


@task(name="update_device_group_status")
def update_device_group_status(locations, vehicles, demands, depot):
    solver = OptimizationService(locations, vehicles, demands, depot)
    opt_route = solver.optimize()


@task(name="update_template_display")
def update_template_display():
    a = 3


@task()
def fetch_all_device_group_statuses():
    municipalities = MunicipalityModel.objects.all().prefetch_related('location__device_group', 'vehicle',
                                                                      'municipality_depot__depot')
    h = list()
    for municipality in municipalities:
        pubsub = PubSubService(municipality.name.replace(' ', '_'))
        ack_id, message = pubsub.pull_from_subscription()
        if message and message.data:
            locations = municipality.location.all()
            vehicles = municipality.vehicle.all()
            depot = municipality.municipality_depot.depot
            group_dem = dict()
            for location in locations:
                demand = DataService.update_device_status(message, location.device_group)
                group_dem[location.device_group.id] = demand
            # pubsub.acknowledge_pull(ack_id)
            update_device_group_status(locations, vehicles, group_dem, depot)
            # h.append(update_device_group_status.s(locations, vehicles, group_dem, depot))

            # chord(group(h))(update_template_display.s())
