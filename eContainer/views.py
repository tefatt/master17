from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


from eContainer.services.input_data_service import InputDataService
from eContainer.services.optimization_service import OptimizationService
from eContainer.models.device import DeviceModel
from eContainer.models.sensor_data import SensorDataModel
from eContainer.models.vehicle import VehicleModel


@csrf_exempt
def update(request):
    values = list()
    if request.data:
        ordered_devices = dict()
        for data in request.data.devices:
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
    OptimizationService(locations,vehicles,demans, settings.DEPOT_LOCATION)





