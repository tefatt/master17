from django.shortcuts import render
from django.http import JsonResponse
from colour import Color

from e_container import tasks
from e_container.services.data_service import DataService


def invocation(request):
    tasks.invocation()


def reset_saved_data(request):
    tasks.reset_saved_data()


def main_display(request):
    return render(request, 'index.html')


def return_new_routes(request):
    markers = DataService.update_map()
    color1, color2 = Color("#19A5A7"), Color("#9119A7")
    path_colors = list(map(Color.get_hex, color1.range_to(color2, len(markers))))
    return JsonResponse({'markers': markers, 'path_colors': path_colors})
