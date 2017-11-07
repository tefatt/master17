from django.db import models
from eContainer.models import BaseModel


class VehicleModel(BaseModel):
    id = models.AutoField(primary_key=True)
    active = models.BooleanField(default=True)
    capacity = models.FloatField()
    type = models.CharField(max_length=225)
    municipality = models.CharField(max_length=225)
