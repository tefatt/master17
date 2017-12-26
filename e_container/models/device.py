from django.db import models
from e_container.models import BaseModel

from e_container.models import DeviceGroupModel


class DeviceModel(BaseModel):
    STANDARD = 0
    DEVICE_TYPES = (
        (STANDARD, "standard"),
    )

    NOT_INSTALLED = 0
    ACTIVE = 1
    BROKEN = 2
    REPAIRED = 3
    DEVICE_STATUSES = (
        (NOT_INSTALLED, "not installed"),
        (ACTIVE, "active"),
        (BROKEN, "broken"),
        (REPAIRED, "repaired"),
    )
    id = models.AutoField(primary_key=True)
    group_id = models.ForeignKey(DeviceGroupModel, null=True, blank=True)
    status = models.IntegerField(choices=DEVICE_STATUSES, default=NOT_INSTALLED)
    max_capacity = models.PositiveIntegerField(help_text='Max capacity of the container it is installed on')
    type = models.IntegerField(choices=DEVICE_TYPES, default=STANDARD)

    def __str__(self):
        return "{} - Type: {}".format(self.id, self.type)


