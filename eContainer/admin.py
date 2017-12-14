from django.contrib import admin

from eContainer.models import *

admin.site.register(DeviceModel)
admin.site.register(DeviceGroupModel)
admin.site.register(VehicleModel)
admin.site.register(EmployeeModel)
admin.site.register(LocationModel)

admin.site.site_header = 'eContainer Administration'
