from django.db import models
from e_container.models import BaseModel
from e_container.models import MunicipalityModel

from e_container.utils.common_utils import CommonUtils


class VehicleModel(BaseModel):
    id = models.AutoField(primary_key=True)
    active = models.BooleanField(default=True)
    capacity = models.FloatField()
    type = models.CharField(max_length=225)
    municipality = models.ForeignKey(MunicipalityModel, related_name='vehicle')
    last_route = models.TextField(editable=False, null=True)


    def __str__(self):
        return "{} - {}".format(self.id, self.type)
