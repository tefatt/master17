from django.conf import settings
import googlemaps
import math

from e_container.services.rrdtool_service import RrdtoolService
from e_container.utils.common_utils import CommonUtils


class DataService:
    def __init__(self):
        pass

    @staticmethod
    def update_device_status(message, device_group):
        rrd = RrdtoolService(str(device_group), device_group.id, )
        try:
            message_body = CommonUtils.decode_request(message.data)
            if message_body.get("device_group") == device_group.id:
                demand = DataService.calculate_group_demand(message_body.get("devices"))
                rrd.update_group({'group_demand': demand})

                # update individual measurements
                for data in message_body.get('devices'):
                    rrd_name = "Device_{} of {}".format(data.get('device_id'), str(device_group))
                    rrd = RrdtoolService(rrd_name, device_group.id)
                    rrd.update_group(data.get("measurements"))
                return demand
        except Exception as e:
            X = True
        return rrd.get_last_value('group_demand')

    @staticmethod
    def calculate_group_demand(device_measurements):
        """Formula for calculating the value for each group location of containers"""

        def scale_measurements(measurements):
            # TODO define scale functions
            result = 0
            for type, value in measurements.items():
                if type == 'ultra_sonic_distance':
                    result += 100 * math.exp(-0.1 * value)
                elif type == 'battery_level':
                    result += 100 * value / (1 + value) if value > 80 else 0
                elif type == 'temperature':
                    result += value
                elif type == 'humidity':
                    result += value
            return result

        demand = 0.
        for data in device_measurements:
            demand += scale_measurements(data.get('measurements'))
        return demand / len(device_measurements)

    @staticmethod
    def calculate_distance(loc1, loc2):
        gmaps = googlemaps.Client(key=settings.GOOGLE_KEY)
        response = gmaps.distance_matrix((loc1[0], loc1[1]), (loc2[0], loc2[1]))
        for property in response.get("rows"):
            # gets distance between two provided locations in meters
            distance = property.get("elements")[0].get("distance").get("value")
            return distance
        return None
