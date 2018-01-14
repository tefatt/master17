from django.conf import settings
import googlemaps
import math

from e_container.services.rrdtool_service import RrdtoolService
from e_container.utils.common_utils import CommonUtils

from e_container.models.device import DeviceModel
from e_container.models.location import LocationModel
from e_container.models.municipality import MunicipalityModel


class DataService:
    def __init__(self):
        pass

    @staticmethod
    def update_device_status(message, device_group):
        rrd = RrdtoolService(str(device_group), device_group.id)
        try:
            message_body = CommonUtils.decode_request(message.data)
            if message_body.get("device_groups"):
                for group in message_body.get("device_groups"):
                    if group.get("id") == device_group.id:
                        demand = DataService.calculate_group_demand(group.get('devices'))
                        rrd.update_group({'group_demand': demand})

                        # update individual measurements
                        for data in group.get('devices'):
                            rrd_name = "Device_{} of {}".format(data.get('device_id'), str(device_group))
                            rrd = RrdtoolService(rrd_name, device_group.id)
                            rrd.update_group(data.get("measurements"))
                        return demand
        except Exception as e:
            X = True
        return rrd.get_last_value('group_demand')

    @staticmethod
    def calculate_group_demand(group):
        """Formula for calculating the value for each group location of containers"""

        def scale_measurements(measurements):
            # TODO define scale functions
            result = 0
            for data_type, value in measurements.items():
                if data_type == 'distance':
                    if value > max_capacity:
                        # in case of bad reading and when testing. Add logging here
                        value = max_capacity
                    result += 100 * math.exp(-1 * (max_capacity - value) / max_capacity)
                elif data_type == 'temperature':
                    pass
                elif data_type == 'humidity':
                    pass
            return result

        demand = 0.
        for data in group:
            max_capacity = DeviceModel.objects.get(id=data.get('device_id')).max_capacity
            device_measurements = data.get('measurements')
            demand += scale_measurements(device_measurements)
        return demand / len(group)

    @staticmethod
    def calculate_distance(from_loc, to_loc, with_duration=False):
        gmaps = googlemaps.Client(key=settings.GOOGLE_KEY)
        response = gmaps.distance_matrix((from_loc[0], from_loc[1]), (to_loc[0], to_loc[1]))
        for field in response.get("rows"):
            # gets distance between two provided locations in meters
            distance = field.get("elements")[0].get("distance").get("value")
            if with_duration:
                duration = field.get("elements")[0].get("duration").get("value")
                return distance, duration
            return distance
        return None

    @staticmethod
    def extract_lat_lon(locs):
        return [(float(loc.latitude), float(loc.longitude)) for loc in locs]

    @staticmethod
    def compute_mean_travel_time(m_id):
        durations = list()
        municipality = MunicipalityModel.objects.get(id=m_id)
        for vehicle in municipality.vehicle.all():
            if vehicle.last_save.route:
                locs = LocationModel.objects.filter(id__in=CommonUtils.str_to_list(vehicle.last_save.route))
                if len(locs) > 1:
                    from_loc, to_loc = (locs[0].latitude, locs[0].longitude), (locs[1].latitude, locs[1].longitude)
                    _, duration = DataService.calculate_distance(from_loc, to_loc, with_duration=True)
                else:
                    duration = None
                durations.append(duration) if duration else 0
        return sum(durations) / len(durations)

    @staticmethod
    def define_start_locations(vehicles, locations, start):
        start_positions = list()
        for vehicle in vehicles:
            route = CommonUtils.str_to_list(vehicle.last_save.route) if hasattr(vehicle, 'last_save') \
                                                                        and vehicle.last_save.route else None
            start_positions.append(route[1]) if route and len(route) > 1 else start_positions.append(start.location.id)

        for i, el in enumerate(locations.values_list('id', flat=True)):
            for j, pos in enumerate(start_positions):
                if el == pos:
                    start_positions[j] = i
                    continue
        return start_positions

    @staticmethod
    def from_ids_to_coordinates(location_ids):
        locations = LocationModel.objects.filter(id__in=location_ids)
        return [(loc.latitude, loc.longitude) for loc in locations]
