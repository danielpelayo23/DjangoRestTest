from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('', views.api_root),
    path('newsletters/', views.NewsletterList.as_view(), name='newsletter-list'),
    path('newsletters/<int:pk>', views.NewsletterDetail.as_view(), name='newsletter-detail'),
    path('subscribers/', views.SubscriberList.as_view(), name='subscriber-list'),
    path('subscribers/<int:pk>', views.SubscriberDetail.as_view(), name='subscriber-detail'),
    path('newsletters/<int:pk>/subscribe', views.SubscribeToNewsletter.as_view(), name='newsletter-subscribe'),
    path('newsletters/<int:pk>/unsubscribe', views.UnsubscribeToNewsletter.as_view(), name='newsletter-unsubscribe'),
    path('activate-subscription/<uuid:pk>', views.ActivateSubscription.as_view(), name='activate-subscription'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
