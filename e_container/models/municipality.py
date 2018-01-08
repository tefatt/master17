from django.db import models
from e_container.models import BaseModel

from e_container.services.pubsub_service import PubSubService


class MunicipalityModel(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    next_invocation = models.DateTimeField(editable=False, null=True)

    def save(self, *args, **kwargs):
        super(MunicipalityModel, self).save(*args, **kwargs)
        PubSubService(self.name.replace(' ', '_'))

    def __str__(self):
        return self.name
