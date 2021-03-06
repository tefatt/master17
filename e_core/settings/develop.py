from __future__ import absolute_import

from .base import *

DEBUG = True

GOOGLE_KEY = 'AIzaSyDTBWlYTjHXsnncux0qHVTroPWt5EWT6YM'
# enter depot location
DEPOT_LOCATION = {}
# defining measurement variable properties with their min and max
RRD_DIRECTORY = 'RRD_files'
ROUTES_DIRECTORY = 'Routes'
# MEASUREMENT_VARIABLES = {'distance': [0, 141], 'temperature': [-10, 60], 'humidity': [0, 20],
#                          'battery_level': [0, 100], 'group_demand': [0, 10]}

MEASUREMENT_VARIABLES = {'distance': [0, 141], 'group_demand': [0, 10]}
# GOOGLE
# os.environ["GOOGLE_CLOUD_PROJECT"] = "econtainer-1498514901196"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = BASE_DIR + '/eContainer-f03bac2d8a5e.json'
GOOGLE_API = {'PROJECT': 'econtainer-1498514901196',
              'DEVICE_DATA_TOPIC': 'projects/econtainer-1498514901196/topics/e_project',
              'DEVICE_DATA_SUBSCRIPTION': 'projects/econtainer-1498514901196/subscriptions/'
              }

# celery
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
from celery.schedules import crontab

# period for examining the status on the field
INVOCATION_PERIOD = 5
RESET_HOURS = '16, 0'
CELERY_BEAT_SCHEDULE = {
    # # Executes every 30min
    # 'pull_from_pubsub': {
    #     'task': 'e_container.tasks.fetch_all_device_group_statuses',
    #     'schedule': crontab(minute='*/30'),
    #     'relative': True
    # },
    'invocation': {
        'task': 'e_container.tasks.invocation',
        'schedule': crontab(minute='*/{}'.format(INVOCATION_PERIOD)),
        'relative': True
    },
    'restart_routes': {
        'task': 'e_container.tasks.reset_saved_routes',
        'schedule': crontab(minute=0, hour=RESET_HOURS),
        'relative': True
    }
}

# # GOOGLE
# GOOGLE_API = {
#     'CLIENT_ID': '493593414963-snd1im5a0k54mtv89ol193igp0bej339.apps.googleusercontent.com',
#     'CLIENT_SECRET': 'w9H9FgJb8WQXfuxMKHfIt-Pu',
#     'SCOPE': ' '.join([
#         'profile',
#         'email',
#         'https://www.googleapis.com/auth/gmail.modify',
#         'https://www.googleapis.com/auth/gmail.readonly',
#         'https://www.googleapis.com/auth/gmail.compose',
#         'https://www.googleapis.com/auth/plus.me',
#         'https://www.googleapis.com/auth/contacts.readonly',
#         'https://www.googleapis.com/auth/drive.readonly',
#         'https://www.googleapis.com/auth/pubsub',
#         'https://www.googleapis.com/auth/calendar'
#     ]),
#     'PUSH_ENDPOINT': 'https://test.getunbox.com/api/services/notifications/',
#     'PROJECT': 'unbox2-174713',
#     'TOPIC': 'projects/unbox2-174713/topics/user-notifications'
# }
