import certifi
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import hashlib
import hmac
import json
import os
from slack_sdk.web import WebClient
from time import time
import ssl as ssl_lib
import sys

incidents = {}
theposted = {}

ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'], ssl=ssl_context)


# Create your views here.

def hash_matches_signature(body, timestamp, signature):
    print("def hash_and_compare")
    prefix = str.encode("v0:" + str(timestamp) + ":")
    signing_secret = os.environ["SLACK_SIGNING_SECRET"]
    request_hash = 'v0=' + hmac.new(
        str.encode(signing_secret),
        prefix + body,
        hashlib.sha256,
    ).hexdigest()

    if hasattr(hmac, "compare_digest"):
        print("if hasattr(hmac, compare_digest)")
        # Compare byte strings for Python 2
        if (sys.version_info[0] == 2):
            print("hmac.compare_digest(bytes(request_hash), bytes(signature))",
                  hmac.compare_digest(bytes(request_hash), bytes(signature)))
            return hmac.compare_digest(bytes(request_hash), bytes(signature))
        else:
            print("hmac.compare_digest(request_hash, signature)", hmac.compare_digest(request_hash, signature))
            return hmac.compare_digest(request_hash, signature)
    else:
        print("else:")
        if len(request_hash) != len(signature):
            print("False")
            return False
        result = 0
        if isinstance(request_hash, bytes) and isinstance(signature, bytes):
            print("the hash is bytes")
            for x, y in zip(request_hash, signature):
                result |= x ^ y
        else:
            print("the hash is not bytes")
            for x, y in zip(request_hash, signature):
                result |= ord(x) ^ ord(y)
        return result == 0


def valid_signature(request):
    print("def valid_signature(request):")
    req_timestamp = request.headers.get('X-Slack-Request-Timestamp')
    req_signature = request.headers.get('X-Slack-Signature')
    print("req_signature: ", req_signature)
    print("req_timestamp: ", req_timestamp)

    if req_timestamp is None:
        print("check timestamp")
        return False

    if req_signature is None:
        print("check signature")
        return False

    if abs(time() - int(req_timestamp)) > 60 * 5:
        print("check timestamp")
        return False

    # Verify the request signature using the app's signing secret
    # emit an error if the signature can't be verified
    return hash_matches_signature(request.body, req_timestamp, req_signature)


def pagerdutywebhook(request):
    print('def pagerdutywebhook(request):')
    if not valid_signature(request):
        return HttpResponseForbidden()

    final_di = json.loads(request.body.decode())
    response = slack_web_client.conversations_list()
    conversations = response['channels']
    channel_ids = {chan['name']: chan['id'] for chan in conversations if chan['is_channel']}

    incidents[final_di["messages"][0]["incident"]["html_url"]] = {
        'incident_number': final_di["messages"][0]["incident"]["incident_number"],
        'status': final_di["messages"][0]["incident"]["status"],
        'title': final_di["messages"][0]["incident"]["title"],
        'service-name': final_di["messages"][0]["incident"]["service"]["name"],
    }

    for k, v in incidents.items():
        if v["service-name"].replace(" ", "-") + "_inc_" + str(v['incident_number']) not in channel_ids.keys():
            response = slack_web_client.conversations_create(
                name=v["service-name"].replace(" ", "-") + "_inc_" + str(v['incident_number']),
                is_private=False,
            )
            channel_ids[v["service-name"].replace(" ", "-") + "_inc_" + str(v['incident_number'])] = \
                response["channel"]["id"]

    # print(json.dumps(incidents, indent=4))

    divider = {
        "type": "divider"
    }

    intro = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*Live Incidents* at *Invitae*"
        },
        "accessory": {
            "type": "image",
            "image_url": "https://s3-media3.fl.yelpcdn.com/bphoto/c7ed05m9lC2EmA3Aruue7A/o.jpg",
            "alt_text": "alt text for image"
        }
    }

    blocks = []

    blocks.append(intro)
    blocks.append(divider)
    for key, value in incidents.items():
        BLOCK = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    value['title'] + "\n\n" \
                    + key + "\n\n" \
                    + " *Status*: " + value['status'] + "\n\n" \
                    + "https://heuristicsteamgroup.slack.com/archives/" + channel_ids[
                        value["service-name"].replace(" ", "-") + "_inc_" + str(v['incident_number'])]
                ),
            },
        }
        blocks.append(BLOCK)
        blocks.append(divider)

    messagel = {
        "ts": "",
        "channel": "C01FC8SKVKJ",
        "username": "",
        "icon_emoji": "",
        "text": final_di["messages"][0]["event"],
        "blocks": blocks
    }

    if "one" in theposted.keys():
        messagel["ts"] = theposted["one"]["message"]["ts"]
        slack_web_client.chat_update(**messagel)
    else:
        theposted["one"] = slack_web_client.chat_postMessage(**messagel)
        messagel["ts"] = theposted["one"]["message"]["ts"]

    return HttpResponse("Hello, world. You're at the polls index. its a function in the app's (polls) views file")


@csrf_exempt
def challenge(request):
    print("def challenge(request)")
    if not valid_signature(request):
        return HttpResponseForbidden()

    # handle the challenge from Slack, which establishes this server as valid in the eyes of the Slack API.
    if request.body:
        final_di = json.loads(request.body.decode())
        if 'challenge' in final_di.keys():
            return HttpResponse(final_di['challenge'])

    return HttpResponse("got it")


def posttoslack(request):
    print("def posttoslack(request)")
    # if not valid_signature(request):
    #     return HttpResponseForbidden()

    NOTIFICATION_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "notification notification"
            ),
        },
    }
    WELCOME_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "This is a post from a django server. :blush:\n\n"
                "*Ich bin nich sicher:*"
            ),
        },
    }

    messagel = {
        "ts": "",
        "channel": "C01FC8SKVKJ",
        "username": "",
        "icon_emoji": "",
        "text": ":pizza:die battieren meines Handys ist fast leer",
        "blocks": [
            NOTIFICATION_BLOCK,
            WELCOME_BLOCK,
        ],
    }

    slack_web_client.chat_postMessage(**messagel)
    return HttpResponse("This is the logic that posts to slack")
