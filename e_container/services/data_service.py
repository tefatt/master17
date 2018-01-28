from django.conf import settings
import googlemaps
import math
from django.db.models import Case, When

from e_container.services.rrdtool_service import RrdtoolService
from e_container.utils.common_utils import CommonUtils

from e_container.models.device import DeviceModel
from e_container.models.location import LocationModel
from e_container.models.municipality import MunicipalityModel
from e_container.models.vehicle import VehicleModel
from e_container.models.employee import EmployeeModel
from e_container.models.recent_data import RecentDataModel


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
                        # abstracted demand can be used later for better prioritization after a route has been generated
                        demand, abstracted_demand = DataService.calculate_group_demand(group.get('devices'))
                        device_group.last_demand = demand
                        device_group.save()
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
            result_volume = 0
            for data_type, value in measurements.items():
                if data_type == 'distance':
                    if value > max_height:
                        # in case of bad reading and when testing. Add logging here
                        value = max_height
                    result += 100 * math.exp(-1 * (max_height - value) / max_height)
                    result_volume += (max_height - value) / 100 * max_surface
                elif data_type == 'temperature':
                    pass
                elif data_type == 'humidity':
                    pass
            return result, result_volume

        demand, real_volume_demand = 0., 0.
        for data in group:
            device = DeviceModel.objects.get(id=data.get('device_id'))
            max_height, max_surface = device.max_height, device.max_surface
            device_measurements = data.get('measurements')
            demand_temp, real_volume_demand_temp = scale_measurements(device_measurements)
            demand += demand_temp
            real_volume_demand += real_volume_demand_temp
        return real_volume_demand, demand / len(group)

    @staticmethod
    def calculate_distance(from_loc, to_loc):
        gmaps = googlemaps.Client(key=settings.GOOGLE_KEY)
        response = gmaps.distance_matrix((from_loc[0], from_loc[1]), (to_loc[0], to_loc[1]))
        for field in response.get("rows"):
            result = field.get("elements")[0]
            # gets distance between two provided locations in meters
            return result.get("distance").get("value"), result.get("duration").get("value")
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
                locs = LocationModel.objects.filter(id__in=CommonUtils.eval_type(vehicle.last_save.route))
                if len(locs) > 1:
                    from_loc, to_loc = (locs[0].latitude, locs[0].longitude), (locs[1].latitude, locs[1].longitude)
                    _, duration = DataService.calculate_distance(from_loc, to_loc)
                else:
                    duration = None
                durations.append(duration) if duration else 0
        return sum(durations) / len(durations)

    @staticmethod
    def define_start_locations(vehicles, location_ids, start):
        start_positions = list()
        for vehicle in vehicles:
            route = CommonUtils.eval_type(vehicle.last_save.route) if hasattr(vehicle, 'last_save') \
                                                                      and vehicle.last_save.route else None
            start_positions.append(route[1]) if route and len(route) > 1 else start_positions.append(start.location.id)

        for i, el in enumerate(start_positions):
            for j, pos in enumerate(location_ids):
                if el == pos:
                    start_positions[i] = j
                    break
        return start_positions

    @staticmethod
    def from_ids_to_coordinates(location_ids):
        locations = LocationModel.objects.filter(id__in=location_ids)
        return [(loc.latitude, loc.longitude) for loc in locations]

    @staticmethod
    def update_map():
        group_locs = list()
        recent_data = RecentDataModel.objects.filter(route__isnull=False)
        routes = recent_data.values_list('route', flat=True)
        vehicle_ids = recent_data.values_list('vehicle', flat=True)
        vehicles = VehicleModel.objects.filter(id__in=vehicle_ids)
        for route in routes:
            route = CommonUtils.eval_type(route)
            if len(route) <= 2:
                continue
            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(route)])
            locs = LocationModel.objects.filter(id__in=route).order_by(preserved)
            group_locs.append(locs.values('id', 'latitude', 'longitude', 'device_group__last_demand'))

        markers = list()
        for locs, vehicle in zip(group_locs, vehicles):
            employee = EmployeeModel.objects.get(vehicle=vehicle)
            marker = list()
            content = "Served by {} driven by {}".format(str(vehicle), str(employee))
            for loc in locs:
                demand_info = "Location id: {} - Demand at group loc: {}  {}".format(loc.get('id'), round(loc.get(
                    'device_group__last_demand'), 2) if loc.get('device_group__last_demand') else None, content)
                info_content = {"coords": {"lat": loc.get('latitude'), "lng": loc.get('longitude')},
                                "content": demand_info}
                marker.append(info_content)
            markers.append(marker)

        return markers
