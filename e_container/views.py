from django.views.decorators.csrf import csrf_exempt

from e_container import tasks


@csrf_exempt
def invocation(request):
    tasks.invocation()


@csrf_exempt
def reset_saved_routes(request):
    tasks.reset_saved_routes()
