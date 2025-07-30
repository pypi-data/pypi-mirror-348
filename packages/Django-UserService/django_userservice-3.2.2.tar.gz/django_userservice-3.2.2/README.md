# django-userservice

[![Build Status](https://github.com/uw-it-aca/django-userservice/workflows/tests/badge.svg)](https://github.com/uw-it-aca/django-userservice/actions)
[![Coverage Status](https://coveralls.io/repos/uw-it-aca/django-userservice/badge.svg?branch=main)](https://coveralls.io/r/uw-it-aca/django-userservice?branch=main)
[![PyPi Version](https://img.shields.io/pypi/v/django-userservice.svg)](https://pypi.python.org/pypi/django-userservice)
![Python versions](https://img.shields.io/pypi/pyversions/django-userservice.svg)

Impersonate users in your application.

To use this - add this to your setting.py's INSTALLED_APPS:

    'userservice',

And this to your MIDDLEWARE_CLASSES:

    'userservice.user.UserServiceMiddleware',

This project uses a function defined in your app to control access to the user override functionality. To use, add this to your settings.py:

    USERSERVICE_OVERRIDE_AUTH_MODULE = 'your_app.module.can_override_user'

If you want to validate the user ids required for override with a local function, add this to your settings.py:

    USERSERVICE_VALIDATION_MODULE='your_app.module.validate_user'

With all of that in place, request.user will be either the actual user, or the user you are impersonating.  To get more information about the current user, you can use:

    user_service = UserService()

    # This is the logged in user's name:
    user_service.get_original_user()

    # This is the override user:
    user_service.get_override_user()

    # This will be the override user if it exists, the logged in user otherwise:
    user_service.get_user()

To make this a dependency for your app, add this to your requirements.txt:

    Django-UserService

or to install, just run:

    pip install Django-UserService
