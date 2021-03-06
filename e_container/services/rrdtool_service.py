import os
from datetime import datetime, timedelta
import rrdtool
from django.conf import settings


class RrdtoolService:
    def __init__(self, rrd_name, dir_name):
        file_path = "{}/Group {}".format(settings.RRD_DIRECTORY, dir_name)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        self.rrd_path = file_path
        self.rrd_name = "{}.rrd".format(rrd_name)
        for variable, interval in settings.MEASUREMENT_VARIABLES.items():
            if self.get_last_value(variable) == 'Non existent':
                first_parameters = ['AVERAGE', 1, 4 * 24]  # one day
                second_parameters = ['AVERAGE', 4, 24 * 30]  # one month
                third_parameters = ['AVERAGE', 4 * 24, 365]  # one year
                for p in [first_parameters, second_parameters, third_parameters]:
                    name = "{}/{} {}".format(file_path, variable, self.rrd_name)
                    RrdtoolService.create_rrd(name, variable, interval[0], interval[1], p[0], p[1], p[2], step='300',
                                              max_absence_time=6 * 60)

    @staticmethod
    def create_rrd(rrd_name, ds_name, min_data, max_data, consolidation_type, units, num_units, start='now',
                   step='900', data_type='GAUGE', max_absence_time=1800, unknown_acceptable_percent=0.4):
        ds_def = "DS:{}:{}:{}:{}:{}".format(ds_name, data_type, max_absence_time, min_data, max_data)
        rra_def = "RRA:{}:{}:{}:{}".format(consolidation_type.upper(), unknown_acceptable_percent, units, num_units)

        rrdtool.create(rrd_name, '--start', start, '--step', step, ds_def, rra_def)

    @staticmethod
    def update_rrd(rrd_name, value):
        value = "N:{}".format(value)
        rrdtool.update(rrd_name, value)

    def get_last_value(self, variable, get_date=False):
        try:
            name = "{}/{} {}".format(self.rrd_path, variable, self.rrd_name)
            last_update = rrdtool.lastupdate(name)
            last_value = last_update.get('ds').get(variable)
            last_value = last_value if last_value else 0
            if get_date:
                return last_value, last_update.get('date')
            else:
                return last_value
        except rrdtool.OperationalError:
            return 'Non existent'

    def update_group(self, values):
        for variable, value in values.items():
            name = "{}/{} {}".format(self.rrd_path, variable, self.rrd_name)
            RrdtoolService.update_rrd(name, value)

    def export_json(self, variable: str, cons_fun: str, dev_group_id: int, start=None, end=None):
        definition = "DEF:data={}/{} {}:{}:{}".format(self.rrd_path, variable, self.rrd_name, variable,
                                                      cons_fun)
        xport_definition = 'XPORT:data:Device Group #{}'.format(dev_group_id)
        if not start and not end:
            now = datetime.now()
            start = int((now - timedelta(hours=1)).timestamp())
            end = int(now.timestamp())

        start_time = "-s {}".format(start)
        end_time = "-e {}".format(end)
        return rrdtool.xport('--json', start_time, end_time, definition, xport_definition)
