from django.contrib import admin
from django import forms

from e_container.models import *

admin.site.register(DeviceModel)
admin.site.register(DeviceGroupModel)
admin.site.register(VehicleModel)
admin.site.register(EmployeeModel)
admin.site.register(LocationModel)
admin.site.register(MunicipalityModel)
admin.site.register(DepotModel)
admin.site.register(MunicipalityDepotModel)

admin.site.site_header = 'e_container Administration'


class LectureForm(forms.ModelForm):
    class Meta:
        model = StartLocationModel
        fields = '__all__'

    def clean(self):
        loc = self.cleaned_data.get('location')
        muni = self.cleaned_data.get('municipality')
        if loc.municipality != muni:
            raise forms.ValidationError("The location must be in the given municipality")
        return self.cleaned_data


class StartLocationAdmin(admin.ModelAdmin):
    form = LectureForm


admin.site.register(StartLocationModel, StartLocationAdmin)
