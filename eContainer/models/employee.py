from django.db import models
from eContainer.models import BaseModel

from eContainer.models import VehicleModel


class EmployeeModel(BaseModel):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    job_title = models.CharField(max_length=225, blank=True, null=True)
    vehicle = models.ForeignKey(VehicleModel)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)



