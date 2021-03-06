# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-08 11:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DepotModel',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DeviceGroupModel',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('last_check_up', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DeviceModel',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.IntegerField(choices=[(0, 'not installed'), (1, 'active'), (2, 'broken'), (3, 'repaired')], default=0)),
                ('max_capacity', models.FloatField(help_text='Max capacity of the container it is installed on')),
                ('type', models.IntegerField(choices=[(0, 'standard')], default=0)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='e_container.DeviceGroupModel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmployeeModel',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=225)),
                ('last_name', models.CharField(max_length=225)),
                ('job_title', models.CharField(blank=True, max_length=225, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LocationModel',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('street', models.CharField(max_length=225)),
                ('street_number', models.CharField(blank=True, help_text='Used for the division of longer streets', max_length=4, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MunicipalityDepotModel',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('depot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='municipality_depot', to='e_container.DepotModel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MunicipalityModel',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('next_invocation', models.DateTimeField(editable=False, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StartLocationModel',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('location', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='start_location', to='e_container.LocationModel')),
                ('municipality', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='start_location', to='e_container.MunicipalityModel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VehicleModel',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=True)),
                ('capacity', models.FloatField()),
                ('type', models.CharField(max_length=225)),
                ('last_route', models.TextField(editable=False, null=True)),
                ('municipality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicle', to='e_container.MunicipalityModel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='municipalitydepotmodel',
            name='municipality',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='municipality_depot', to='e_container.MunicipalityModel'),
        ),
        migrations.AddField(
            model_name='locationmodel',
            name='municipality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location', to='e_container.MunicipalityModel'),
        ),
        migrations.AddField(
            model_name='employeemodel',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_container.VehicleModel'),
        ),
        migrations.AddField(
            model_name='devicegroupmodel',
            name='employee_check_up',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_container.EmployeeModel'),
        ),
        migrations.AddField(
            model_name='devicegroupmodel',
            name='location',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='device_group', to='e_container.LocationModel'),
        ),
        migrations.AddField(
            model_name='depotmodel',
            name='location',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='depot', to='e_container.LocationModel'),
        ),
    ]
