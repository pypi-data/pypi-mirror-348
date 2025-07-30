# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.module_loading import import_string
from django.shortcuts import render


def can_override_user(request):
    print("Your application should define an authorization function "
          "as USERSERVICE_OVERRIDE_AUTH_MODULE in settings.py.")
    return False


def override_admin_required(view_func):
    """
    View decorator that checks whether the user is permitted to override
    (act as) users. Calls login_required in case the user is not authenticated.
    """
    def wrapper(request, *args, **kwargs):
        func_str = getattr(
            settings, 'USERSERVICE_OVERRIDE_AUTH_MODULE',
            'userservice.decorators.can_override_user')
        auth_func = import_string(func_str)

        if auth_func(request):
            return view_func(request, *args, **kwargs)

        return render(request, 'no_access.html', status=401)

    return login_required(function=wrapper)
