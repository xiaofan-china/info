"""
Django settings for web project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*=!2hn(lm=en)g!g5z$&dpvg=lxgeu43_d-z1*8wk^95ca*^)w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#DEBUG = False

TEMPLATE_DEBUG = False

#add RequestContext processors

ALLOWED_HOSTS = ["*"]

#ADMIN_MEDIA_PREFIX="/static/grappelli/"
# Application definition
INSTALLED_APPS = (
    'south',
    'django_admin_bootstrapped.bootstrap3',
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'web01',
    #'web02',
	'vpn',
    'django.contrib.humanize',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
SESSION_COOKIE_AGE=36000
SESSION_SAVE_EVERY_REQUEST=True
SESSION_ENGINE='django.contrib.sessions.backends.file'
SESSION_FILE_PATH="/tmp/django/"
ROOT_URLCONF = 'web.urls'

WSGI_APPLICATION = 'web.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS':{
            'init_command':'set storage_engine=INNODB',
        },
        'NAME':'web01',
	    'USER':'django',
	    'PASSWORD':'django2',
	    'HOST':'10.18.6.123',
	    'PORT':'3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT="/apps/product/tengine/html/zan/static_collect"
AUTHENTICATION_BACKENDS=(
'web01.views.Myauth',
)
