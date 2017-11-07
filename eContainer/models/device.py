from django.db import models
from eContainer.models import BaseModel

from eContainer.models import LocationModel
from eContainer.models import EmployeeModel

DEVICE_TYPES = (
    (0, "standard"),
)


class DeviceModel(BaseModel):
    id = models.AutoField(primary_key=True)
    group_id = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)
    max_capacity = models.PositiveIntegerField()
    type = models.IntegerField(choices=DEVICE_TYPES, default=0)
    employee_check_up = models.ForeignKey(EmployeeModel)
    last_check_up = models.DateField()
    location = models.ForeignKey(LocationModel)


