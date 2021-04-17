"""
These settings configure the Gunicorn master and worker processes.

In configuring Gunicorn, we can read the Django settings. :)

Available settings are here: https://docs.gunicorn.org/en/stable/settings.html#

This particular settings file is taken from examples in Gunicorn project
https://github.com/benoitc/gunicorn/blob/master/examples/read_django_settings.py


Basic Usage for this config file as defined in the Gunicorn project:

reference this config file as you start your gunicorn processes:

    $ gunicorn project_name.wsgi:application -c read_django_settings.py

For Incident Manager, that translates to

    (see start_incident_manager.sh)
"""

settings_dict = {}

with open('incident/settings_prod.py') as f:
    exec(f.read(), settings_dict)

loglevel = 'info'
proc_name = 'Incident-Manager'
workers = 20
bind = 'localhost:8000'

if settings_dict['DEBUG']:
    loglevel = 'debug'
    reload = True
    proc_name += '_debug'
