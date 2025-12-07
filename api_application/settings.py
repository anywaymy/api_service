
# Содержит основные настройки
# (конфигурация приложений, шаблонов, middleware...)

import os
from email.policy import default
from pathlib import Path
from decouple import config
# from django.conf.global_settings import INSTALLED_APPS

# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Секрет кей для безопасности
SECRET_KEY = config('SECRET_KEY')

# Режим отладки
DEBUG = config('DEBUG', default=False, cast=bool)

# Указываем домены, на которых будет работать наш сайт
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*').split(',')

# Список встроенных Django приложения
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Список сторонних приложений
THIRD_PARTY_APPS = [
    'rest_framework',
]

# Список наших приложений
LOCAL_APPS = [
    'apps.core',
]

# Общий список
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# Список middleware для обработки запросов
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Корневой Url файл проекта
ROOT_URLCONF = 'api_application.urls'

# Конфигурация шаблоново Джанго
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'api_application.wsgi.application'


# Конфигурация БД
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


#Конфигурация БД
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB', default='api_app'),
        'USER': config('POSTGRES_USER', default='api_app'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432', cast=int),
        'ATOMIC_REQUESTS': True,
    }
}

# Валидаторы паролей
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Настройка интернациональности
LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Настройка статических файлов
STATIC_URL = 'static/' # url статики
STATIC_ROOT = BASE_DIR / 'staticfiles' # путь для собранных файлов статики


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Разрешить доступ всем
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',  # Ограничение запросов для анонимных пользователей
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',  # Лимит запросов для анонимных пользователей
    },
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',  # Рендеринг в JSON
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',  # Парсинг JSON-данных
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'apps.core.authentication.CsrfExemptSessionAuthentication', # в рамках проекта отключил csrf защиту
        'rest_framework.authentication.BasicAuthentication',
    ],
}


# Настройки безопасности
SECURE_BROWSER_XSS_FILTER = True  # Защита от XSS-атак
SECURE_CONTENT_TYPE_NOSNIFF = True  # Запрет MIME-типов
X_FRAME_OPTIONS = 'DENY'  # Защита от кликджекинга

# Настройки логирования
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',  # Уровень логирования
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
