from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse

from e_container import tasks
from e_container.utils.common_utils import CommonUtils
from e_container.services.data_service import DataService
from e_container.models.vehicle import VehicleModel
from e_container.models.recent_data import RecentDataModel
from e_container.models.location import LocationModel


def invocation(request):
    tasks.invocation()


def reset_saved_routes(request):
    tasks.reset_saved_routes()


def main_display(request):
    group_locs = list()
    routes = RecentDataModel.objects.filter(route__isnull=False).values_list('route', flat=True)
    for route in routes:
        route = CommonUtils.str_to_list(route)
        if len(route) < 2:
            continue
        locs = LocationModel.objects.filter(id__in=route).values('latitude', 'longitude')
        group_locs.append(locs)
    # locs = [(43.845339, 18.324240), (43.848971, 18.390119), (43.851477, 18.397374), (43.858378, 18.426112),
    #         (43.858324, 18.406673), (43.866448, 18.340083)]

    vehs = ['Vehicle 1.']
    markers = list()
    for locs in group_locs:
        marker = list()
        [marker.append({"coords": {"lat": loc.get('latitude'), "lng": loc.get('longitude')}}) for loc in locs]
        markers.append(marker)

    return render(request, 'index.html', {'markers': markers})


def return_new_routes(request):
    # locs = [(43.845339, 18.324240), (43.848971, 18.390119), (43.851477, 18.397374), (43.858378, 18.426112),
    #         (43.858324, 18.406673), (43.866448, 18.340083)]
    # with open('ajax_check.txt', 'r') as f:
    #     x = f.read()
    # if 'DOSAO' == x:
    #     locs = [(43.855663, 18.388419), (43.848971, 18.390119), (43.851477, 18.397374), (43.858378, 18.426112),
    #             (43.858324, 18.406673), (43.866448, 18.340083)]
    # markers = [{"coords": {"lat": loc[0], "lng": loc[1]}} for loc in locs]
    # with open('ajax_check.txt', 'w') as f:
    #     f.write('DOSAO')
    group_locs = list()
    routes = RecentDataModel.objects.filter(route__isnull=False).values_list('route', flat=True)
    for route in routes:
        route = CommonUtils.str_to_list(route)
        if len(route) < 2:
            continue
        locs = LocationModel.objects.filter(id__in=route).values('latitude', 'longitude')
        group_locs.append(locs)

    vehs = ['Vehicle 1.']
    markers = list()
    for locs in group_locs:
        marker = list()
        [marker.append({"coords": {"lat": loc.get('latitude'), "lng": loc.get('longitude')}}) for loc in locs]
        markers.append(marker)

    return JsonResponse({'markers': markers})
