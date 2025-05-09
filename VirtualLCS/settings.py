import os
from pathlib import Path
import dj_database_url
from decouple import config


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['mydetour-e22e7c03c4e8.herokuapp.com','e05e-2c0f-fe38-2325-b1e3-edd8-8d40-19dd-f7eb.ngrok-free.app','localhost', '127.0.0.1', '[::1]']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Coordinator',
    'Discussion',
    'channels',#to enable audio interaction in screenshares through handling web sockets
    'debug_toolbar',
    'webpack_loader', #integrate react with django
    # 'sslserver',
]

ASGI_APPLICATION = 'VirtualLCS.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
            "capacity": 10000,  # Number of messages in the queue
            "expiry": 60,       # Message expiry time in seconds
        },
    },
}

# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             'hosts': [os.getenv('REDIS_URL')],
#             "capacity": 10000,
#             "expiry": 60,
#         },
#     },
# }

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'frontend/',
        'STATS_FILE': os.path.join(BASE_DIR, 'frontend', 'webpack-stats.json'),
    }
}



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'VirtualLCS.middlewares.RootRedirectMiddleware',  # Include your custom middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'VirtualLCS.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),  # Django templates folder
            os.path.join(BASE_DIR, 'frontend/build')      # React build folder
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'VirtualLCS.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('NAME'),
        'USER': config('USER'),
        'PASSWORD': config('PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# DATABASES = {
#     'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
# }


AUTH_USER_MODEL = 'Coordinator.CustomUser'


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator','OPTIONS': {'min_length': 8}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Ensure it's using standard user authentication
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# This directory is where collectstatic will gather all the static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


STATIC_URL = '/static/'
# STATICFILES_DIRS = [BASE_DIR, 'static']
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static/coordinator'),  # Include your static folder here
    os.path.join(BASE_DIR, 'frontend/build/static'),  # Include React's static files
    os.path.join(BASE_DIR, 'frontend/build/')  # Include React's static files
]


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INTERNAL_IPS = [
    "127.0.0.1",
]

TEMPLATES[0]['OPTIONS']['context_processors'].append('django.template.context_processors.request')

# TEMPLATES[0]['DIRS'] = [BASE_DIR / "templates"]
TEMPLATES[0]['DIRS'] = [os.path.join(BASE_DIR, "templates")]



LOGIN_URL = '/Coordinator/login/'  # Your custom login page
LOGIN_REDIRECT_URL = '/Coordinator/dashboard/'  # Redirect after successful login

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')


# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# SECURE_SSL_REDIRECT = True  # Redirect all HTTP traffic to HTTPS
# SESSION_COOKIE_SECURE = True  # Use HTTPS for session cookies
# CSRF_COOKIE_SECURE = True  # Use HTTPS for CSRF cookies

# DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage' 
# AZURE_ACCOUNT_NAME = config('AZURE_ACCOUNT_NAME')
# AZURE_ACCOUNT_KEY = config('AZURE_ACCOUNT_KEY')
# AZURE_CONTAINER = 'media'