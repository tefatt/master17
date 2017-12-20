from django.db import models
from e_container.models import BaseModel

from e_container.models import LocationModel
from e_container.models import EmployeeModel

from e_container.services.pubsub_service import PubSubService


class DeviceGroupModel(BaseModel):
    id = models.AutoField(primary_key=True)
    location = models.ForeignKey(LocationModel)
    last_check_up = models.DateField()
    employee_check_up = models.ForeignKey(EmployeeModel)

    def save(self, *args, **kwargs):
        super(DeviceGroupModel, self).save(*args, **kwargs)
        PubSubService(str(self).replace(' ', '_'))

    def __str__(self):
        return "Group {} at {} {}".format(str(self.id), self.location.street, self.location.street_number)
