from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
import json
from django.db.models import Q

from e_container import tasks
from e_container.utils.common_utils import CommonUtils
from e_container.services.pubsub_service import PubSubService
from e_container.services.rrdtool_service import RrdtoolService
from e_container.services.data_service import DataService
from e_container.models.municipality import MunicipalityModel
from e_container.models.device_group import DeviceGroupModel
from e_container.models.vehicle import VehicleModel


def invocation(request):
    prefixs = '/Users/teufiktutundzic/Desktop/master17/JSON measurement test/'
    data_files = [prefixs + 'Novo Sarajevo.json', prefixs + 'Novi Grad.json']
    municipalities_names = ['NOVO_SARAJEVO', 'NOVI_GRAD']
    for data, mun_name in zip(data_files, municipalities_names):
        data = json.load(open(data))
        data = str(data).encode('utf-8')

        pubsub = PubSubService(mun_name)
        pubsub.publish(data)
    tasks.invocation()


def reset_saved_data(request):
    tasks.reset_saved_data()


def main_display(request):
    municipalities = MunicipalityModel.objects.all().values('id', 'name')
    for mun in municipalities:
        device_groups = DeviceGroupModel.objects.filter(location__municipality_id=mun['id']). \
            values('id', 'location__street', 'location__street_number')
        mun['device_groups'] = list(device_groups)
        vehicles = VehicleModel.objects.filter(Q(municipality=mun['id']), Q(last_save__demand__gt=0))
        mun['vehicle_indexes'] = [i for i, veh in enumerate(vehicles)]
    mun_markers = DataService.update_map()
    return render(request, 'index.html', {'municipalities': list(municipalities), 'mun_markers': mun_markers})


def return_new_routes(request):
    mun_markers = DataService.update_map()
    return JsonResponse({'mun_markers': mun_markers})


def return_route(request):
    mun_name = request.GET.get('mun_name')
    if not mun_name:
        return HttpResponseBadRequest
    route_index = request.GET.get('route_index', 0)
    markers = DataService.fetch_route(mun_name, route_index)
    return JsonResponse({'markers': markers})


def data_readings(request):
    dev_group_id = request.GET.get('dev_group_id')
    device_group = DeviceGroupModel.objects.get(id=CommonUtils.eval_type(dev_group_id))
    rrd = RrdtoolService(str(device_group), device_group.id)
    x = rrd.get_last_value('group_demand', get_date=True)
    measurements = rrd.export_json('group_demand', 'AVERAGE', dev_group_id)
    measurements = [
        [10206117003, 4000000000e+00],
        [10206120003, 4000000000e+00],
        [10206123003, 4000000000e+00],
        [10206126003, 4113333333e+00],
        [10206129003, 4000000000e+00],
        [10206132003, 4000000000e+00],
        [10206135003, 4000000000e+00],
        [10206138003, 4000000000e+00],
        [10206141003, 4000000000e+00],
        [10206144003, 4000000000e+00],
        [10206147003, 7333333333e+00],
        [10206150003, 4000000000e+00],
        [10206153003, 4000000000e+00]]

    return render(request, 'flot_rrd.html', {'location': str(device_group.location), 'measurements': measurements})
