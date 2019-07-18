from kombu import Exchange, Queue

from .base import *  # noqa


# Broker settings
BROKER_URL = get_env_var('BROKER_URL', 'amqp://guest:guest@localhost//')

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ALWAYS_EAGER = get_env_var('CELERY_ALWAYS_EAGER', 'False') == 'True'

CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE_TYPE = 'direct'
CELERY_DEFAULT_ROUTING_KEY = 'default'

# http://docs.celeryproject.org/en/latest/configuration.html#celery-queues
CELERY_QUEUES = (
    Queue('default', Exchange('clinic', type='direct'), routing_key='default'),
)

CELERYBEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'

# http://docs.celeryproject.org/en/latest/configuration.html#celery-routes
# CELERY_ROUTES = {}

# Whether to store the task return values or not.
CELERY_IGNORE_RESULT = True

# If you still want to store errors, just not successful return values
CELERY_STORE_ERRORS_EVEN_IF_IGNORED = False

ROOT_URLCONF = 'restbucks.urls.panel'
