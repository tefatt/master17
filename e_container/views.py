from django.shortcuts import render
from django.http import JsonResponse

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
    return JsonResponse({'markers': markers})
