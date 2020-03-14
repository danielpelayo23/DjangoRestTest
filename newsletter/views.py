from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveAPIView, \
    RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from .models import Newsletter, Subscriber, SubscriberNewsletter
from .serializers import NewsletterSerializer, SubscriberSerializer


@api_view(['GET'])
def api_root(request):
    return Response({
        'subscribers': reverse('subscriber-list', request=request),
        'newsletters': reverse('newsletter-list', request=request)
    })


class NewsletterDetail(RetrieveUpdateAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer


class NewsletterList(ListCreateAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer


class SubscriberList(ListAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer


class SubscriberDetail(RetrieveAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer


class SubscribeToNewsletter(APIView):
    @staticmethod
    def _get_newsletter(pk):
        try:
            return Newsletter.objects.get(pk=pk)
        except Newsletter.DoesNotExist:
            raise Http404

    def post(self, request, pk):
        newsletter = self._get_newsletter(pk)
        serializer = SubscriberSerializer(data=request.data)
        if serializer.is_valid():
            subscriber = Subscriber.objects.filter(email=serializer.validated_data['email']).first()
            if subscriber:
                for (key, value) in serializer.validated_data.items():
                    setattr(subscriber, key, value)
                subscriber.save()
            else:
                subscriber = serializer.save()
            if not bool(newsletter.subscribers.filter(id=subscriber.id)):
                newsletter.subscribe(subscriber)
                subscription = SubscriberNewsletter.objects.filter(newsletter=newsletter, subscriber=subscriber).first()
                response = serializer.data
                response.update({'subscription_id': subscription.id})
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response({"message": "email already registered"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnsubscribeToNewsletter(APIView):
    @staticmethod
    def _get_newsletter(pk):
        try:
            return Newsletter.objects.get(pk=pk)
        except SubscriberNewsletter.DoesNotExist:
            raise Http404

    def post(self, request, pk):
        newsletter = self._get_newsletter(pk)
        newsletter.unsubscribe(*newsletter.subscribers.filter(email=request.data['email']))
        return Response(status=status.HTTP_200_OK)


class ActivateSubscription(APIView):
    @staticmethod
    def _get_subscription(pk):
        try:
            return SubscriberNewsletter.objects.get(pk=pk)
        except SubscriberNewsletter.DoesNotExist:
            raise Http404

    def post(self, request, pk):
        subscription = self._get_subscription(pk)
        subscription.is_active = True
        subscription.save()
        return Response(status=status.HTTP_200_OK)
