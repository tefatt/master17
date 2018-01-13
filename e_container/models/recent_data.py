from django.db import models
from e_container.models import BaseModel
from e_container.models import VehicleModel


class RecentDataModel(BaseModel):
    id = models.AutoField(primary_key=True)
    vehicle = models.OneToOneField(VehicleModel, related_name='last_save')
    route = models.TextField(editable=False, null=True)
    demand = models.FloatField(editable=False, null=True)
    distance = models.FloatField(editable=False, null=True)

    def __str__(self):
        return "{} - {}".format(self.route, self.vehicle)
