from django.test import TestCase

from ..models import Newsletter, Subscriber


class NewsletterTest(TestCase):

    def setUp(self):
        self.newsletter = Newsletter.objects.create(name='Newsletter 1')
        self.subscriber_1 = Subscriber.objects.create(name='Subscriber 1', email='test1@examle.com')
        self.subscriber_2 = Subscriber.objects.create(name='Subscriber 1', email='test2@examle.com')
        self.newsletter.subscribe(self.subscriber_1)

    def test_subscribe(self):
        self.newsletter.subscribe(self.subscriber_2)
        self.assertEqual(len(self.newsletter.subscribers.all()), 2)

    def test_unsubscribe(self):
        self.newsletter.unsubscribe(self.subscriber_1)
        self.assertEqual(len(self.newsletter.subscribers.all()), 0)
