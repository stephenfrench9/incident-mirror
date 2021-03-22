# Slack App

# Local Development Environment

## Secrets

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

## Trigger the endpoint designed to accept the PagerDuty webhook.

```
curl -H "Content-Type: application/json" --data @incident-trigger-request-body.json http:/127.0.0.1:8000/incident-manager/accept-pagerduty-webhook/
curl -H "Content-Type: application/json" --data @incident-trigger-request-body-2.json http://127.0.0.1:8000/incident-manager/accept-pagerduty-webhook/
```

# Staging environment

## Secrets
same as above

## start the ec2 server
```
cd /Users/stephen.french/terratrials/ec2
terraform apply
terraform output public_ip
export PUBLIC_IP=$(terraform output public_ip)
terraform output ssh
eval $(terraform output ssh)
ssh -i "stephens-new-shiny-public-key.pem" ec2-user@ec2-34-238-244-81.compute-1.amazonaws.com
```

## Bootstrap the ec2 server
```
brew install git
sudo apt-install git-all
sudo dnf install git-all
sudo dnf install git-all
sudo dnf install git-all
sudo su
git clone git@github.com:stephenfrench9/incident-mirror.git
git clone https://github.com/stephenfrench9/incident-mirror.git
pip install
lsb_release -a
yum install python3.7
sudo su
sudo git fetch && git reset --hard origin/$(git rev-parse --abbrev-ref HEAD)
git log --oneline -4
```

## start Django server
```
# from root of this repo
cd incident
pip install requirements.txt
python3 manage.py runserver 0.0.0.0:8000
```

## Query the PagerDuty API and display results
```
curl -v http://$PUBLIC_IP:8000/incident-manager/pd-api/
```

## Post to Slack
```
curl -v http://$PUBLIC_IP:8000/incident-manager/post-to-slack/
```

## Trigger the endpoint designed to accept the PagerDuty webhook.
#### you have to go poke a hole in the firewall before pagerduty can post to Incident Manager

PagerDuty previously followed a policy of (Safelisting IP Addresses)[https://support.pagerduty.com/docs/safelisting-ips]

They have enabled (TLS 1.2)[https://developer.pagerduty.com/docs/webhooks/webhooks-mutual-tls/]

For now, you go poke a hole in the firewall so that PD can post to the EC2 instance

```
curl -v http://$PUBLIC_IP:8000/incident-manager/accept-pagerduty-webhook/
curl -H "Content-Type: application/json" --data @incident-trigger-request-body.json http://$PUBLIC_IP:8000/incident-manager/accept-pagerduty-webhook/
curl -H "Content-Type: application/json" --data @incident-trigger-request-body-2.json http://$PUBLIC_IP:8000/incident-manager/accept-pagerduty-webhook/
```
