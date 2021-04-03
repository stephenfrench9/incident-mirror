"""
taken from examples in Gunicorn project
https://github.com/benoitc/gunicorn/blob/master/examples/read_django_settings.py

Use this config file in your script like this:

    $ gunicorn project_name.wsgi:application -c read_django_settings.py

For Incident Manager, that translates to

    (see start_incident_manager.sh)
"""

settings_dict = {}

with open('incident/settings_prod.py') as f:
    exec(f.read(), settings_dict)

loglevel = 'info'
proc_name = 'web-project'
workers = 1

if settings_dict['DEBUG']:
    loglevel = 'debug'
    reload = True
    proc_name += '_debug'
