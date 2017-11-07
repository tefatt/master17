from django.db import models
from eContainer.models import BaseModel


class LocationModel(BaseModel):
    id = models.AutoField(primary_key=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    street = models.CharField(max_length=225)
    municipality = models.CharField(max_length=225)
