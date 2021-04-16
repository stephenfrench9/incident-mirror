from django.urls import path

from . import views

urlpatterns = [
    # /incident-manager/accept-pagerduty-webhook/
    path('accept-pagerduty-webhook/', view=views.pagerduty_webhook, name='pagerdutywebhook'),

    # /incident-manager/post-to-slack/
    path('post-to-slack/', view=views.post_to_slack, name='post_to_slack'),

    # /incident-manager/challenge/
    path('challenge/', view=views.challenge, name='challenge'),

    # /incident-manager/pdapi/
    path('pd-api/', view=views.pd_api, name='pd_api'),

    # /incident-manager/write/
    path('write/', view=views.write, name='write'),

    # /incident-manager/read/
    path('read/', view=views.read, name='read'),
]
