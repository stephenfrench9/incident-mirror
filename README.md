#Slack App

## Prepare Environment

```
export SLACK_SIGNING_SECRET=""
export SLACK_BOT_TOKEN=""
export INCIDENT_MANAGER_PAGERDUTY_API_ACCESS_KEY=""
```

[SLACK_SIGNING_SECRET can be found here](https://api.slack.com/apps/A01NKJX118Q/general?)
[SLACK_BOT_TOKEN can be found here](https://api.slack.com/apps/A01NKJX118Q/oauth?)
[INCIDENT_MANAGER_PAGERDUTY_API_ACCESS_KEY can be found here](https://dev-invitae.pagerduty.com/api_keys)

## Start the Django Server

```
# from root of this repo
cd incident
pip install requirements.txt
python3 manage.py runserver
```

## Query the PagerDuty API and display results

```
curl -v http://127.0.0.1:8000/incident-manager/pd-api/
```
or surf to http://127.0.0.1:8000/incident-manager/pd-api/ in Google Chrome

This endpoint is currently configured to return a list of all Users in the account.

## Post to Slack

```
curl -v http://127.0.0.1:8000/incident-manager/post-to-slack/
```

or surf to http://127.0.0.1:8000/incident-manager/post-to-slack/ in Google Chrome

This endpoint is currently configured to post a simple message to a Slack channel in the Heuristics workspace.
