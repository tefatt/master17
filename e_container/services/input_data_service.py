from django.conf import settings
import googlemaps

from e_container.services.rrdtool_service import RrdtoolService

from e_container.utils.common_utils import CommonUtils
from e_container.models.device import DeviceModel
from e_container.models.device_group import DeviceGroupModel


class InputDataService:
    def __init__(self):
        pass

    @staticmethod
    def update_device_status(message):
        values = list()
        if message.body:
            request_body = CommonUtils.decode_request(message.body)
            ordered_devices = dict()
            dg = DeviceGroupModel.objects.get(id=request_body.get("device_group"))
            # RrdtoolService.create_rrd(str(dg), 'UltraSonicDistance', 0, 100, 'AVERAGE', 1, 48)
            rrd = RrdtoolService(str(dg))
            for data in request_body.get('devices'):
                rrd.update_group(data.get("measurements"))
                # RrdtoolService.update_rrd(str(dg), data.get("measurements").get("distance"))
                value = rrd.get_last_value()
                device = DeviceModel.objects.get(id=data.get("device_id"))
                if device.group_id not in ordered_devices.keys():
                    ordered_devices[device.group_id] = list()
                ordered_devices[device.group_id].append((measurements, device))
            for group_id, device_data in ordered_devices.items():
                value = InputDataService.calculate_group_demand(device_data[0])
                device_properties = (value, device_data[1].location, device_data[1].active)
                values.append({group_id: device_properties})
        # TODO this goes to a template
        return values

    # @staticmethod
    # def calculate_group_demand(measurements):
    #     """Formula for calculating the value for each group location of containers"""
    #     return value

    @staticmethod
    def calculate_distance(location1, location2):
        gmaps = googlemaps.Client(key=settings.GOOGLE_KEY)
        response = gmaps.distance_matrix(location1, location2)
        for property in response.get("rows"):
            # gets distance between two provided locations in meters
            distance = property.get("elements")[0].get("distance").get("value")
            return distance
        return None
