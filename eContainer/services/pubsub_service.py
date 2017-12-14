from google.cloud import pubsub
from  google.api_core.exceptions import AlreadyExists
from django.conf import settings


class PubSubService:
    def __init__(self, topic):
        self.publisher = pubsub.PublisherClient()
        self.topic = 'projects/{project_id}/topics/{topic}'.format(
            project_id=settings.GOOGLE_API['PROJECT'],
            topic=topic)
        try:
            self.publisher.create_topic(self.topic)
        except AlreadyExists:
            pass

    def test_connection(self):
        self.publisher.publish(self.topic, b'First message!', spam='smth')
