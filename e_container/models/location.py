from django.db import models
from e_container.models import BaseModel


class LocationModel(BaseModel):
    id = models.AutoField(primary_key=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    street = models.CharField(max_length=225)
    street_number = models.CharField(max_length=4, null=True)
    municipality = models.CharField(max_length=225)

    def __str__(self):
        return "{} {} - {}".format(self.street, self.street_number, self.municipality)

