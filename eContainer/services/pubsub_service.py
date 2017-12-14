from google.cloud import pubsub
from  google.api_core.exceptions import AlreadyExists
from django.conf import settings


class PubSubService:
    def __init__(self, device_group):
        self.publisher = pubsub.PublisherClient()
        self.subscriber = pubsub.SubscriberClient()
        try:
            self.subscriber.create_subscription(
                "{}{}".format(settings.GOOGLE_API['DEVICE_DATA_SUBSCRIPTION'], device_group),
                settings.GOOGLE_API['DEVICE_DATA_TOPIC'])
        except AlreadyExists:
            pass

    def test_connection(self):
        self.publisher.publish(settings.GOOGLE_API['DEVICE_DATA_TOPIC'], b'Test message!', spam='smth')
