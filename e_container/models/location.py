from django.db import models
from e_container.models import BaseModel
from e_container.models import MunicipalityModel


class LocationModel(BaseModel):
    id = models.AutoField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    street = models.CharField(max_length=225)
    street_number = models.CharField(max_length=4, null=True, blank=True,
                                     help_text='Used for the division of longer streets')
    municipality = models.ForeignKey(MunicipalityModel, related_name='location')

    def __str__(self):
        return "{} {} - {}".format(self.street, self.street_number, self.municipality) if self.street_number else \
            "{} - {}".format(self.street, self.municipality)
