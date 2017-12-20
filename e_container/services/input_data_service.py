from django.conf import settings
import googlemaps
import rrdtool

from e_container.utils.common_utils import CommonUtils
from e_container.models.device import DeviceModel


class InputDataService:
    def __init__(self):
        pass

    @staticmethod
    def update_device_status(message):
        with open('/Users/teufiktutundzic/Desktop/master17/somefileX.txt', 'a') as the_file:
            the_file.write('ALOHA\n')
            the_file.write(str(message) + '\n')
        values = list()
        if message.body:
            request_body = CommonUtils.decode_request(message.body)
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

