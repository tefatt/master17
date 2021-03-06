# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-15 16:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_container', '0002_auto_20180112_2047'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicegroupmodel',
            name='last_demand',
            field=models.FloatField(editable=False, null=True),
        ),
        migrations.RemoveField(
            model_name='devicemodel',
            name='max_capacity',
        ),
        migrations.AddField(
            model_name='devicemodel',
            name='max_height',
            field=models.FloatField(default=141,
                                    help_text="Max height of the container it's installed on. Unit of measurement is cm"),
        ),
        migrations.AddField(
            model_name='devicemodel',
            name='max_surface',
            field=models.FloatField(default=1.096,
                                    help_text='Max surface area of the respective container. Unit of measurement is m2'),
        ),
        migrations.AlterField(
            model_name='vehiclemodel',
            name='capacity',
            field=models.FloatField(help_text='Unit of measurement is m3'),
        ),
    ]
