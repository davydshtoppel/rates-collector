from .common import *

import os


SECRET_KEY = 'ip8x7v(vmlug3zu+pqix_5@zw)&4ku@+dvv(rr&fw9q7m4m1wd'

DEBUG = False

ALLOWED_HOSTS = ["localhost",  "127.0.0.1", "hedwig", "192.168.0.108", "colrates-proxy", "colrates"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': f"{os.getenv('DATABASE_NAME')}",
        'ATOMIC_REQUESTS': 'True',
        "USER": f"{os.getenv('DATABASE_USER')}",
        "PASSWORD": f"{os.getenv('DATABASE_PASSWORD')}",
        "HOST": f"{os.getenv('DATABASE_HOST')}",
        "PORT": f"{os.getenv('DATABASE_PORT')}",
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
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
        'rates.views': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}
