import os
import rrdtool
from django.conf import settings


class RrdtoolService:
    def __init__(self, rrd_name, dir_name):
        file_path = "{}/Group {}".format(settings.RRD_DIRECTORY, dir_name)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        self.rrd_path = file_path
        self.rrd_name = "{}.rrd".format(rrd_name)
        if not self.get_last_value():
            first_parameters = ['AVERAGE', 1, 2 * 24]
            second_parameters = ['MAX', 1, 2 * 24]
            third_parameters = ['AVERAGE', 1, 2 * 24 * 30]
            for variable, interval in settings.MEASUREMENT_VARIABLES.items():
                for p in [first_parameters, second_parameters, third_parameters]:
                    name = "{}/{} {}".format(file_path, variable.upper(), self.rrd_name)
                    RrdtoolService.create_rrd(name, variable, interval[0], interval[1], p[0], p[1], p[2])

    @staticmethod
    def create_rrd(rrd_name, ds_name, min_data, max_data, consolidation_type, units, consolidations, start='now',
                   step='18000', data_type='GAUGE', max_absence_time=2400, unknown_acceptable_percent=0.4):
        ds_def = "DS:{}:{}:{}:{}:{}".format(ds_name, data_type, max_absence_time, min_data, max_data)
        rra_def = "RRA:{}:{}:{}:{}".format(consolidation_type.upper(), unknown_acceptable_percent, units,
                                           consolidations)

        rrdtool.create(rrd_name, '--start', start, '--step', step, ds_def, rra_def)

    @staticmethod
    def update_rrd(rrd_name, value):
        value = "N:{}".format(value)
        rrdtool.update(rrd_name, value)

    def get_last_value(self):
        try:
            return rrdtool.lastupdate(self.rrd_name)
        except rrdtool.OperationalError:
            return None

    def update_group(self, values):
        for variable, value in values.items():
            name = "{}/{} {}".format(self.rrd_path, variable.upper(), self.rrd_name)
            RrdtoolService.update_rrd(name, value)
