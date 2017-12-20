from google.cloud import pubsub
from google.api_core.exceptions import AlreadyExists
from django.conf import settings


class PubSubService:
    def __init__(self, device_group, topic=settings.GOOGLE_API['DEVICE_DATA_TOPIC']):
        self.publisher = pubsub.PublisherClient()
        self.subscriber = pubsub.SubscriberClient()
        try:
            self.topic = topic
            self.subscription = "{}{}".format(settings.GOOGLE_API['DEVICE_DATA_SUBSCRIPTION'], device_group)
            self.subscriber.create_subscription(self.subscription, topic)
        except AlreadyExists:
            pass

    def test_connection(self):
        self.publisher.publish(settings.GOOGLE_API['DEVICE_DATA_TOPIC'], b'Test message!')

    def pull_from_subscription(self, callback):
        pull = self.subscriber.subscribe(self.subscription)
        pull.open(callback)

