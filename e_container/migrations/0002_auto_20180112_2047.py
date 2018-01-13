# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-12 20:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('e_container', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecentDataModel',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('route', models.TextField(editable=False, null=True)),
                ('demand', models.FloatField(editable=False, null=True)),
                ('distance', models.FloatField(editable=False, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='vehiclemodel',
            name='last_route',
        ),
        migrations.AddField(
            model_name='recentdatamodel',
            name='vehicle',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='last_save', to='e_container.VehicleModel'),
        ),
    ]
