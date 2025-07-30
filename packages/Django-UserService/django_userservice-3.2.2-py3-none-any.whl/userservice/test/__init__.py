# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.contrib.auth.models import User


def get_user(username):
    try:
        user = User.objects.get(username=username)
        return user
    except Exception as ex:
        user = User.objects.create_user(username, password='pass')
        return user


def can_override(request):
    return True


def add_washington(username):
    return "{}@uw.edu".format(username)


def under8(username):
    if len(username) < 8:
        return None
    return "Bad len"


def over8(username):
    if len(username) > 8:
        return None
    return "Bad len"
