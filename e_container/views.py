from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from e_container.services.input_data_service import InputDataService
from e_container.services.optimization_service import OptimizationService
from e_container.services.pubsub_service import PubSubService
from e_container.utils.common_utils import CommonUtils
from e_container.models.device import DeviceModel
from e_container.models.vehicle import VehicleModel


@csrf_exempt
def update(request):
    pubsub = PubSubService('Group_1_at_Hifzi_Bjelevca_64')
    pubsub.pull_from_subscription(InputDataService.update_device_status)
    values = list()
    if request.body:
        request_body = CommonUtils.decode_request(request.body)
        ordered_devices = dict()
        for data in request_body.get('devices'):
            device = DeviceModel.objects.get(id=data.get("device_id"))
            measurements = SensorDataModel.objects.create(defaults=data.get("measurements"))
            if device.group_id not in ordered_devices.keys():
                ordered_devices[device.group_id] = list()
            ordered_devices[device.group_id].append((measurements, device))
        for group_id, device_data in ordered_devices.items():
            value = InputDataService.calculate_group_demand(device_data[0])
            device_properties = (value, device_data[1].location, device_data[1].active)
            values.append({group_id: device_properties})
    # TODO this goes to a template
    return values


def vehicle_routing(municipality):
    devices = DeviceModel.objects.filter(location__municipality=municipality)
    ordered_devices = dict()
    for device in devices:
        if device.group_id not in ordered_devices.keys():
            ordered_devices[device.group_id] = list()
        ordered_devices[device.group_id].append(device)
    locations = ordered_devices.values_list("locations")
    vehicles = VehicleModel.objects.filter(municipality=municipality)
    OptimizationService(locations, vehicles, demans, settings.DEPOT_LOCATION)
