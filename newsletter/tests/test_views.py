from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Newsletter, Subscriber, SubscriberNewsletter
from ..serializers import NewsletterSerializer, SubscriberSerializer


class NewsletterViewsTest(APITestCase):

    def setUp(self):
        self.url = '/newsletters/'
        self.newsletter = Newsletter.objects.create(name='Newsletter 1')

    def test_create_newsletter(self):
        response = self.client.post(self.url, {'name': 'test newsletter'})
        newsletter = Newsletter.objects.get(pk=response.data['id'])
        serializer = NewsletterSerializer(newsletter)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_fetch_newsletters(self):
        response = self.client.get(self.url)
        newsletters = Newsletter.objects.all()
        serializer = NewsletterSerializer(newsletters, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_newsletter(self):
        response = self.client.get(self.url + str(self.newsletter.pk))
        newsletter = Newsletter.objects.get(pk=self.newsletter.pk)
        serializer = NewsletterSerializer(newsletter)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_newsletter(self):
        response = self.client.put(self.url + str(self.newsletter.pk), {'name': 'new name'})
        newsletter = Newsletter.objects.get(pk=self.newsletter.pk)
        serializer = NewsletterSerializer(newsletter)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SubscriberViewsTest(APITestCase):

    def setUp(self):
        self.url = '/subscribers/'
        self.subscriber = Subscriber.objects.create(name='Subscriber 1', email='test1@examle.com')

    def test_fetch_subscribers(self):
        response = self.client.get(self.url)
        subscribers = Subscriber.objects.all()
        serializer = SubscriberSerializer(subscribers, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_subscriber(self):
        response = self.client.get(self.url + str(self.subscriber.pk))
        subscriber = Subscriber.objects.get(pk=self.subscriber.pk)
        serializer = SubscriberSerializer(subscriber)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SubscriptionViewsTest(APITestCase):

    def setUp(self):
        self.url = '/newsletters/{}/'
        self.newsletter = Newsletter.objects.create(name='Newsletter 1')
        self.subscriber = Subscriber.objects.create(name='Subscriber 1', email='test1@examle.com')
        self.newsletter.subscribe(self.subscriber)
        self.subscription = SubscriberNewsletter.objects.get(newsletter=self.newsletter, subscriber=self.subscriber)

    def test_subscribe(self):
        response = self.client.post(
            self.url.format(self.newsletter.pk) + 'subscribe', {'name': 'John', 'email': 'john@example.com'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.newsletter.subscribers.all()), 2)

    def test_unsubscribe(self):
        response = self.client.post(
            self.url.format(self.newsletter.pk) + 'unsubscribe', {'email': 'test1@examle.com'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.newsletter.subscribers.all()), 0)

    def test_activate_subscription(self):
        self.assertFalse(self.subscription.is_active)
        response = self.client.post(
            f'/activate-subscription/{str(self.subscription.pk)}'
        )
        self.subscription.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.subscription.is_active)
