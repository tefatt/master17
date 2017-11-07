from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^update/', views.update, name='update_url'),
]