from google.cloud import pubsub
from google.api_core.exceptions import AlreadyExists
from django.conf import settings


class PubSubService:
    def __init__(self, municipality):
        self.publisher = pubsub.PublisherClient()
        self.subscriber = pubsub.SubscriberClient()
        try:
            self.topic = "{}_{}".format(settings.GOOGLE_API['DEVICE_DATA_TOPIC'], municipality.upper())
            self.publisher.api.create_topic(self.topic)
        except AlreadyExists:
            pass
        try:
            self.subscription = "{}{}".format(settings.GOOGLE_API['DEVICE_DATA_SUBSCRIPTION'], municipality.upper())
            self.subscriber.api.create_subscription(self.subscription, self.topic, ack_deadline_seconds=10)
        except AlreadyExists:
            pass

    def publish(self, data):
        self.publisher.publish(settings.GOOGLE_API['DEVICE_DATA_TOPIC'], data=data)

    def pull_from_subscription(self):
        pull = self.subscriber.api.pull(subscription=self.subscription, max_messages=1, return_immediately=True)
        if not pull.received_messages:
            return None, None
        return pull.received_messages[0].ack_id, pull.received_messages[0].message

    def acknowledge_pull(self, ack_id):
        self.subscriber.api.acknowledge(ack_ids=[ack_id], subscription=self.subscription)

