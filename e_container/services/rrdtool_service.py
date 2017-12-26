import rrdtool
from django.conf import settings


class RrdtoolService:
    def __init__(self, rrd_name):
        self.rrd_name = "{}.rrd".format(rrd_name)

    @staticmethod
    def create_rrd(rrd_name, ds_name, min_data, max_data, consolidation_type, units, consolidations, start='now',
                   step='18000', data_type='GAUGE', max_absence_time=2400, unknown_acceptable_percent=0.4):
        rrd_name = "{}.rrd".format(rrd_name)
        ds_def = "DS:{}:{}:{}:{}:{}".format(ds_name, data_type, max_absence_time, min_data, max_data)
        rra_def = "RRA:{}:{}:{}:{}".format(consolidation_type.upper(), unknown_acceptable_percent, units,
                                           consolidations)

        rrdtool.create(rrd_name, '--start', start, '--step', step, ds_def, rra_def)

    @staticmethod
    def update_rrd(rrd_name, value):
        rrd_name += '.rrd'
        value = "N:{}".format(value)
        rrdtool.update(rrd_name, value)

    def get_last_value(self):
        return rrdtool.lastupdate(self.rrd_name)

    def define_group_rrd(self):
        first_parameters = ['AVERAGE', 1, 2 * 24]
        second_parameters = ['COUNTER', 1, 2 * 24]
        third_parameters = ['AVERAGE', 1, 2 * 24 * 30]
        for variable, interval in settings.MEASUREMENT_VARIABLES.items():
            for p in [first_parameters, second_parameters, third_parameters]:
                name = "{}/{}".format(variable, self.rrd_name)
                RrdtoolService.create_rrd(name, variable, interval[0], interval[1], p[0], p[1], p[2])

    def update_group(self, values):
        for variable, value in values:
            name = "{}/{}".format(variable, self.rrd_name)
            RrdtoolService.update_rrd(name, value)
