from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from e_container.services.data_service import DataService
from e_container.services.optimization_service import OptimizationService
from e_container.services.pubsub_service import PubSubService
from e_container import tasks
from e_container.services.rrdtool_service import RrdtoolService
from e_container.utils.common_utils import CommonUtils
from e_container.models.device import DeviceModel
from e_container.models.vehicle import VehicleModel
from e_container.models.device_group import DeviceGroupModel
from e_container.models.location import LocationModel
import rrdtool
from datetime import datetime


@csrf_exempt
def update(request):
    # pubsub = PubSubService('Group_1_at_Hifzi_Bjelevca_64')
    # pubsub.pull_from_subscription(InputDataService.update_device_status)

    tasks.update_device_group_status()
    values = list()
    if request.body:
        request_body = CommonUtils.decode_request(request.body)
        dg = DeviceGroupModel.objects.get(id=request_body.get("device_group"))
        dg.recent_demand = DataService.calculate_group_demand(request_body.get("devices"))

        l = LocationModel.objects.all()
        v = VehicleModel.objects.all()
        dem = [0, 19, 21, 6, 19]
        OptimizationService(l, v, dem, 0)

        with open('/Users/teufiktutundzic/Desktop/master17/somefileX.txt', 'a') as the_file:
            the_file.write('ENTERED\n')
            the_file.write(str(request_body) + '\n')
        ordered_devices = dict()
        dg = DeviceGroupModel.objects.get(id=request_body.get("device_group"))
        RrdtoolService.create_rrd(str(dg), 'UltraSonicDistance', 0, 100, 'AVERAGE', 1, 48)
        for data in request_body.get('devices'):
            RrdtoolService.update_rrd(str(dg), data.get("measurements").get("distance"))
            device = DeviceModel.objects.get(id=data.get("device_id"))
            if device.group_id not in ordered_devices.keys():
                ordered_devices[device.group_id] = list()
            ordered_devices[device.group_id].append((measurements, device))
        for group_id, device_data in ordered_devices.items():
            value = DataService.calculate_group_demand(device_data[0])
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
