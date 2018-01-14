from celery import task
from celery import chord, group
from datetime import datetime, timedelta

from django.conf import settings
from e_container.services.pubsub_service import PubSubService
from e_container.services.data_service import DataService
from e_container.services.optimization_service import OptimizationService

from e_container.models.municipality import MunicipalityModel
from e_container.models.depot import DepotModel
from e_container.models.vehicle import VehicleModel
from e_container.models.recent_data import RecentDataModel


@task(name="update_device_group_status")
def update_device_group_status(locations, vehicles, demands, depot, municipality):
    solver = OptimizationService(locations, vehicles, demands, depot, municipality.start_location)
    optimized_route_data = solver.optimize()
    eta = DataService.compute_mean_travel_time(municipality.id)
    municipality.next_invocation = timedelta(seconds=eta) + datetime.now()
    municipality.save()
    return optimized_route_data


@task()
def fetch_all_device_group_statuses(municipality):
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
        update_device_group_status(locations, vehicles, group_dem, depot, municipality)
        # chord(update_device_group_status.s(locations, vehicles, group_dem, depot))(update_template_display.s())


@task()
def invocation():
    municipalities = MunicipalityModel.objects.all().prefetch_related('location__device_group', 'vehicle__last_save',
                                                                      'municipality_depot__depot', 'start_location')
    execute_municipalities = list()
    ago = datetime.now() - timedelta(minutes=settings.INVOCATION_PERIOD)
    ahead = datetime.now() + timedelta(minutes=settings.INVOCATION_PERIOD)
    for m in municipalities:
        # if not m.next_invocation or (ago <= m.next_invocation <= ahead):
        fetch_all_device_group_statuses(m)
        #         execute_municipalities.append(fetch_all_device_group_statuses.s(m))
        # group(execute_municipalities).get()


@task()
def reset_saved_routes():
    RecentDataModel.objects.filter(vehicle__active=True).update(route=None, demand=None, distance=None)
