from celery import task

from e_container.services.pubsub_service import PubSubService
from e_container.services.data_service import DataService
from e_container.models.municipality import MunicipalityModel


@task()
def update_device_group_status():
    group_demands = dict()
    municipalities = MunicipalityModel.objects.all().prefetch_related('location__device_group')
    for municipality in municipalities:
        pubsub = PubSubService(municipality.name.replace(' ', '_'))
        ack_id, message = pubsub.pull_from_subscription()
        if message and message.data:
            for location in municipality.location.all():
                demand = DataService.update_device_status(message, location.device_group)
                if demand:
                    group_demands[location.device_group.id] = demand
            pubsub.acknowledge_pull(ack_id)

    x = 'asa'
