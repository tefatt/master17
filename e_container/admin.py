from django.contrib import admin

from e_container.models import *

admin.site.register(DeviceModel)
admin.site.register(DeviceGroupModel)
admin.site.register(VehicleModel)
admin.site.register(EmployeeModel)
admin.site.register(LocationModel)

admin.site.site_header = 'e_container Administration'
