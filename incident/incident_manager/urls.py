from django.urls import path

from . import views

urlpatterns = [
    # /incident-manager/accept-pagerduty-webhook/
    path('accept-pagerduty-webhook/', view=views.pagerdutywebhook, name='pagerdutywebhook'),

    # /incident-manager/post-to-slack/
    path('post-to-slack/', view=views.posttoslack, name='posttoslack'),

    # /incident-manager/challenge/
    path('challenge/', view=views.challenge, name='challenge'),
]
