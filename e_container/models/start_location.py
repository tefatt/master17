from django.db import models
from e_container.models import BaseModel
from e_container.models import LocationModel
from e_container.models import MunicipalityModel


class StartLocationModel(BaseModel):
    id = models.AutoField(primary_key=True)
    location = models.OneToOneField(LocationModel, related_name='start_location')
    municipality = models.OneToOneField(MunicipalityModel, related_name='start_location')

    def __str__(self):
        return "Start location: {}".format(str(self.location))
