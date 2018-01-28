from django.db import models
from e_container.models import BaseModel

from e_container.services.rrdtool_service import RrdtoolService
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
    group = models.ForeignKey(DeviceGroupModel, null=True, blank=True)
    status = models.IntegerField(choices=DEVICE_STATUSES, default=NOT_INSTALLED)
    max_surface = models.FloatField(default=1.096,
                                    help_text="Max surface area of the respective container. Unit of measurement is m2")
    max_height = models.FloatField(default=141,
                                   help_text="Max height of the container it's installed on. Unit of measurement is cm")
    type = models.IntegerField(choices=DEVICE_TYPES, default=STANDARD)

    def save(self, *args, **kwargs):
        super(DeviceModel, self).save(*args, **kwargs)
        RrdtoolService("Device_{} of {}".format(self.id, str(self.group)), self.group.id)
        RrdtoolService(str(self.group), self.group.id)

    def __str__(self):
        return "Device {}: {} - Capacity: {}m3".format(self.id, self.group, self.max_height / 100 * self.max_surface)
