from .common import *

import os

SECRET_KEY = 'ip8x7v(vmlug3zu+pqix_5@zw)&4ku@+dvv(rr&fw9q7m4m1wd'

DEBUG = False

ALLOWED_HOSTS = ["localhost",  "127.0.0.1"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'colrates',
        'ATOMIC_REQUESTS': 'True',
        "USER": "shtodav",
        "PASSWORD": "secret",
        "HOST": "postgres",
        "PORT": "5432",
    }
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} {levelname} {module} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'root': {
            'handlers': ['console'],
            'propagate': True,
        },
    }
}
