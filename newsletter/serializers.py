from rest_framework import serializers

from .models import Subscriber, Newsletter


class SubscriberSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    email = serializers.CharField()

    def create(self, validated_data):
        return Subscriber.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()


class NewsletterSerializer(serializers.ModelSerializer):
    subscribers = SubscriberSerializer(many=True, read_only=True)

    class Meta:
        model = Newsletter
        fields = ['id', 'name', 'subscribers']
