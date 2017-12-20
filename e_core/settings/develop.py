from __future__ import absolute_import

from .base import *

DEBUG = True

GOOGLE_KEY = 'AIzaSyDTBWlYTjHXsnncux0qHVTroPWt5EWT6YM'
# enter depot location
DEPOT_LOCATION = {}

# GOOGLE
# os.environ["GOOGLE_CLOUD_PROJECT"] = "econtainer-1498514901196"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = BASE_DIR + '/eContainer-f03bac2d8a5e.json'
GOOGLE_API = {'PROJECT': 'econtainer-1498514901196',
              'DEVICE_DATA_TOPIC': 'projects/econtainer-1498514901196/topics/device_data',
              'DEVICE_DATA_SUBSCRIPTION': 'projects/econtainer-1498514901196/subscriptions/'
              }

# celery
os.environ['PYTHON_PATH'] = '/Users/teufiktutundzic/env_eContainer/lib/python3.6/site-packages'

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    # Executes every 30min
    'pull_from_pubsub': {
        'task': 'e_container.tasks.update_device_group_status',
        'schedule': crontab(minute='*/30'),
        'relative': True
    },
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
