import os
from .settings import *
import settings 


ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else ['*']
CSRF_TRUSTED_ORIGINS = ['https://'+ os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []

STATIC_HOST = 'https://'+ os.environ['WEBSITE_HOSTNAME']+'.azurewebsites.net/'
STATIC_URL = STATIC_HOST + "/static/"

connection_string = os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']
parameter = {pair.split('=')[0] : pair.split('=')[1] for pair in connection_string.split(' ')}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': parameter['dbname'],
        'HOST': parameter['host'],
        'USER': parameter['user'],
        'PASSWORD': parameter['password'],
        'PORT' : parameter['port'] 
    }
}
# Email send the user (email server)
# EMAIL_HOST = 'smtpout.secureserver.net'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

settings.MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']