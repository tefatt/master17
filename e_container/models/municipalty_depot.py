from django.db import models
from e_container.models import BaseModel
from e_container.models import MunicipalityModel
from e_container.models import DepotModel


class MunicipalityDepotModel(BaseModel):
    id = models.AutoField(primary_key=True)
    municipality = models.OneToOneField(MunicipalityModel, related_name='municipality_depot')
    depot = models.ForeignKey(DepotModel, related_name='municipality_depot')

    def __str__(self):
        return "{}: {}".format(str(self.municipality), str(self.depot))
