from .base import *

DEBUG = True

# Secret key only for local
SECRET_KEY = '2=1y(#1g1cqhmb8o=wt2$-)#b8ysf1&vle4nq)8w0rmtplq$%&'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'restbucks',
        'HOST': 'localhost',
        'USER': 'mohammad',
        'PASSWORD': 'habitt',
        'PORT': '5432'
    }
}
