import os
from .settings import *
import settings 


settings.ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []
CSRF_TRUSTED_ORIGINS = ['https://'+ os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []

STATIC_HOST = 'https://'+ os.environ['WEBSITE_HOSTNAME']+'.azurewebsites.net/'
STATIC_URL = STATIC_HOST + "/static/"


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DBNAME'],
        'HOST': os.environ['DBHOST'],
        'USER': os.environ['USER'],
        'PASSWORD': os.environ['PASSWORD'],
        'PORT' : os.environ['PORT'], 
    }
}
# Email send the user (email server)
# EMAIL_HOST = 'smtpout.secureserver.net'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']