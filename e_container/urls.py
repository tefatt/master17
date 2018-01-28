from django.conf.urls import url, include

from . import views

app_name = 'eContainer'

urlpatterns = [
    url(r'^invocation/', views.invocation, name='invocation'),
    url(r'^reset_saved_data/', views.reset_saved_data, name='reset_saved_data'),
    url(r'^main_display/', views.main_display, name='main_display'),
    url(r'^return_new_routes/', views.return_new_routes, name='return_new_routes'),
    url(r'^data_readings/', views.data_readings, name='data_readings')
]
