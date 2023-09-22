import os
from .settings import *
from .settings import BASE_DIR, MIDDLEWARE, DEBUG

if DEBUG:
    DEBUG = False
    ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []
CSRF_TRUSTED_ORIGINS = ['https://'+ os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []


hostname = os.environ['DBHOST']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DBNAME'],
        'HOST': hostname + ".postgres.database.azure.com",
        'USER': os.environ['DBUSER'],
        'PASSWORD': os.environ['DBPASS'] 
    }
}
# Email send the user (email server)
# EMAIL_HOST = 'smtpout.secureserver.net'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
ALLOWED_HOSTS = ["*"]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MIDDLEWARE += 'whitenoise.middleware.WhiteNoiseMiddleware',