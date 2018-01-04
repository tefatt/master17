from django.db import models
from e_container.models import BaseModel
from e_container.models import LocationModel


class DepotModel(BaseModel):
    id = models.AutoField(primary_key=True)
    location = models.OneToOneField(LocationModel, related_name='depot')

    def __str__(self):
        return str(self.location)
