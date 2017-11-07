from django.db import models
from eContainer.models import BaseModel
from eContainer.models.device import DeviceModel


class SensorDataModel(BaseModel):
    id = models.AutoField(primary_key=True)
    fullness = models.PositiveIntegerField()
    battery_level_percent = models.PositiveIntegerField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    device = models.ForeignKey(DeviceModel)


