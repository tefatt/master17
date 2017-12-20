from django.db import models
from e_container.models import BaseModel


class VehicleModel(BaseModel):
    id = models.AutoField(primary_key=True)
    active = models.BooleanField(default=True)
    capacity = models.FloatField()
    type = models.CharField(max_length=225)
    municipality = models.CharField(max_length=225)

    def __str__(self):
        return "{} - {}".format(self.id, self.type)

