from django.db import models
from e_container.models import BaseModel

from e_container.models import LocationModel
from e_container.models import EmployeeModel


class DeviceGroupModel(BaseModel):
    id = models.AutoField(primary_key=True)
    location = models.OneToOneField(LocationModel, related_name='device_group')
    last_check_up = models.DateField()
    employee_check_up = models.ForeignKey(EmployeeModel)
    last_demand = models.FloatField(editable=False, null=True)

    def __str__(self):
        return "Group_{} at {}-{}".format(self.id, self.location.street, self.location.municipality.name)
