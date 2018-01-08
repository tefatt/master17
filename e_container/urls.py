from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^invocation/', views.invocation, name='invocation'),
    url(r'^reset_saved_routes/', views.reset_saved_routes, name='reset_saved_routes'),
]
