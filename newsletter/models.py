import uuid

from django.db import models


class Subscriber(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)


class Newsletter(models.Model):
    name = models.CharField(max_length=120, unique=True)
    subscribers = models.ManyToManyField(Subscriber, through='SubscriberNewsletter')

    def subscribe(self, *subscriber):
        self.subscribers.add(*subscriber)

    def unsubscribe(self, *subscriber):
        self.subscribers.remove(*subscriber)


class SubscriberNewsletter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
