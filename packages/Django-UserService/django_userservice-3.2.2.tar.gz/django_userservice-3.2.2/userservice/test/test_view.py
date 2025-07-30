# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from unittest import skipIf
from django.test import TestCase
from django.conf import settings
from django.test import Client
from django.test.client import RequestFactory
from django.test.utils import override_settings
from django.urls import reverse
from userservice.test import get_user as get_django_user
from userservice.user import get_user, get_acting_user, get_override_user
from userservice.user import get_original_user, set_override_user


def missing_url(name):
    try:
        url = reverse(name)
    except Exception as ex:
        print(ex)
        return True
    return False


@override_settings(
    MIDDLEWARE=[
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.RemoteUserMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ],
    AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.ModelBackend'],
)
class TestView(TestCase):

    @skipIf(missing_url("userservice_override"), "URLs not configured")
    def test_cannot_override(self):
        c = Client()
        get_django_user('javerage')
        c.login(username='javerage', password='pass')
        request = RequestFactory().get("/")
        request.session = c.session
        request.user = get_django_user('javerage')
        response = c.post(reverse("userservice_override"),
                          {"override_as": "testover"})
        self.assertEqual(response.status_code, 401)

    @skipIf(missing_url("userservice_override"), "URLs not configured")
    @override_settings(
        USERSERVICE_OVERRIDE_AUTH_MODULE='userservice.test.can_override')
    def test_override(self):
        c = Client()

        get_django_user('javerage')
        c.login(username='javerage', password='pass')

        request = RequestFactory().get("/")
        request.session = c.session
        request.user = get_django_user('javerage')

        response = c.post(reverse("userservice_override"),
                          {"override_as": "testover"})
        request.session = c.session

        self.assertEqual(get_user(request), 'testover')
        self.assertEqual(get_acting_user(request), 'javerage')
        self.assertEqual(get_original_user(request), 'javerage')
        self.assertEqual(get_override_user(request), 'testover')

        response = c.post(reverse("userservice_override"),
                          {"clear_override": 1})

        request = RequestFactory().get("/")
        request.session = c.session

        self.assertEqual(get_user(request), 'javerage')
        self.assertEqual(get_acting_user(request), 'javerage')
        self.assertEqual(get_original_user(request), 'javerage')
        self.assertEqual(get_override_user(request), None)

    @skipIf(missing_url("userservice_override"), "URLs not configured")
    @override_settings(
        USERSERVICE_OVERRIDE_AUTH_MODULE='userservice.test.can_override')
    def test_async_override(self):
        c = Client()

        get_django_user('javerage')
        c.login(username='javerage', password='pass')

        request = RequestFactory().get('/')
        request.session = c.session
        request.user = get_django_user('javerage')

        headers = {"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}
        response = c.post(
            reverse("userservice_override"), {"override_as": "testover"},
            content_type='application/json', **headers)
        request.session = c.session

        self.assertEqual(get_user(request), 'testover')
        self.assertEqual(get_acting_user(request), 'javerage')
        self.assertEqual(get_original_user(request), 'javerage')
        self.assertEqual(get_override_user(request), 'testover')

        response = c.post(
            reverse("userservice_override"), {"clear_override": 1},
            content_type='application/json', **headers)

        request = RequestFactory().get("/")
        request.session = c.session

        self.assertEqual(get_user(request), 'javerage')
        self.assertEqual(get_acting_user(request), 'javerage')
        self.assertEqual(get_original_user(request), 'javerage')
        self.assertEqual(get_override_user(request), None)

    @override_settings(
        USERSERVICE_OVERRIDE_AUTH_MODULE='userservice.test.can_override',
        USERSERVICE_VALIDATION_MODULE='userservice.test.under8')
    def test_validation(self):
        c = Client()

        get_django_user('javerage')
        c.login(username='javerage', password='pass')

        request = RequestFactory().get("/")
        request.session = c.session
        request.user = get_django_user('javerage')

        response = c.post(reverse("userservice_override"),
                          {"override_as": "testover8"})

        self.assertEqual(get_user(request), 'javerage')
        self.assertEqual(get_acting_user(request), 'javerage')
        self.assertEqual(get_original_user(request), 'javerage')
        self.assertEqual(get_override_user(request), None)

    @override_settings(
        USERSERVICE_OVERRIDE_AUTH_MODULE='userservice.test.can_override',
        USERSERVICE_VALIDATION_MODULE='userservice.test.over8')
    def test_validation2(self):
        c = Client()

        get_django_user('javerage')
        c.login(username='javerage', password='pass')

        request = RequestFactory().get("/")
        request.session = c.session
        request.user = get_django_user('javerage')

        response = c.post(reverse("userservice_override"),
                          {"override_as": "testover8"})

        self.assertEqual(get_user(request), 'testover8')
        self.assertEqual(get_acting_user(request), 'javerage')
        self.assertEqual(get_original_user(request), 'javerage')
        self.assertEqual(get_override_user(request), 'testover8')

    @override_settings(
        USERSERVICE_OVERRIDE_AUTH_MODULE='userservice.test.can_override',
        USERSERVICE_TRANSFORMATION_MODULE='userservice.test.add_washington')
    def test_transform(self):
        c = Client()

        get_django_user('javerage')
        c.login(username='javerage', password='pass')

        request = RequestFactory().get("/")
        request.session = c.session
        request.user = get_django_user('javerage')

        response = c.post(reverse("userservice_override"),
                          {"override_as": "testover8"})

        self.assertEqual(get_user(request), 'testover8@uw.edu')
        self.assertEqual(get_acting_user(request), 'javerage')
        self.assertEqual(get_original_user(request), 'javerage')
        self.assertEqual(get_override_user(request), 'testover8@uw.edu')
