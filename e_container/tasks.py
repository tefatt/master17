from celery import task

from e_container.services.pubsub_service import PubSubService
from e_container.services.input_data_service import InputDataService
from e_container.models.device_group import DeviceGroupModel


@task()
def update_device_group_status():
    import os

    with open('/Users/teufiktutundzic/Desktop/master17/somefile.txt', 'a') as the_file:
        the_file.write('NOVO\n')
        the_file.write(os.environ.get('PYTHON_PATH'))

        for device_group in DeviceGroupModel.objects.all():
            pubsub = PubSubService(str(device_group).replace(' ', '_'))
            pubsub.pull_from_subscription(InputDataService.update_device_status)

            pubsub.test_connection()