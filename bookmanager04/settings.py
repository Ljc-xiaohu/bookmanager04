"""
Django settings for bookmanager04 project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')*dfghdz5sr@@#&&9b19om8(05u@dh_fv(t^h8l(6(+9c+r4cj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'book.apps.BookConfig',
    'rest_framework',  # 使用DRF（Django REST framework,全称djangorestful-framework）必须注册
    'django_filters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bookmanager04.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'bookmanager04.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',  # 数据库主机
        'PORT': 3306,  # 数据库端口
        'USER': 'root',  # 数据库用户名
        'PASSWORD': 'mysql',  # 数据库用户密码
        'NAME': 'book_16_04'  # 数据库名字
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

# LANGUAGE_CODE = 'en-us'
#
# TIME_ZONE = 'UTC'

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'


# 我们在settings中进行配置,所以的视图都采用这个设置
REST_FRAMEWORK = {

    #认证的设置
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # BasicAuthentication
        #此身份验证方案使用HTTP基本身份验证，
        # 根据用户的用户名和密码进行签名。
        # 基本身份验证通常仅适用于测试
        # 'rest_framework.authentication.BasicAuthentication',

        #SessionAuthentication  session认证
        'rest_framework.authentication.SessionAuthentication',
    ),

    # #权限

    # IsAuthenticated 所有的视图 必须通过认证 (session认证)
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),   #不同的设置中间记得加,  逗号


    # 可选限流类
    # 1） AnonRateThrottle限制所有匿名未认证用户，使用IP区分用户。
    # 使用DEFAULT_THROTTLE_RATES['anon']来设置频次

    # 2）UserRateThrottle限制认证用户，使用User id 来区分。
    # 使用DEFAULT_THROTTLE_RATES['user']来这是频次

    # 3）ScopedRateThrottle限制用户对于每个视图的访问频次，使用ip或user id。

    # # 限流
    # 'DEFAULT_THROTTLE_CLASSES': (
    #     'rest_framework.throttling.AnonRateThrottle',
    #     'rest_framework.throttling.UserRateThrottle'
    # ),
    # 'DEFAULT_THROTTLE_RATES': {
    #     'anon': '3/day',
    #     'user': '10/day'
    # }


    # 'DEFAULT_THROTTLE_CLASSES': (
    #     'rest_framework.throttling.ScopedRateThrottle',
    # ),
    # 'DEFAULT_THROTTLE_RATES': {
    #     'contacts': '3/day',
    #     'uploads': '20/day'
    # }

    # 过滤设置
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
}
