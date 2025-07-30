# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import TestCase
from django.conf import settings
from django.test.client import RequestFactory

from userservice.test import get_user as get_django_user
from userservice.user import get_user, get_acting_user, get_override_user
from userservice.user import get_original_user, set_override_user
from userservice.user import clear_override, UserService, UserServiceMiddleware


class TestAPI(TestCase):
    def test_basic(self):
        request = RequestFactory().get("/")
        request.session = {}

        self.assertEqual(get_user(request), None)
        self.assertEqual(get_acting_user(request), None)
        self.assertEqual(get_override_user(request), None)
        self.assertEqual(get_original_user(request), None)

    def test_user(self):
        request = RequestFactory().get("/")
        request.session = {}
        request.user = get_django_user('javerage')

        self.assertEqual(get_user(request), 'javerage')
        self.assertEqual(get_acting_user(request), 'javerage')
        self.assertEqual(get_override_user(request), None)
        self.assertEqual(get_original_user(request), 'javerage')

    def test_override(self):
        request = RequestFactory().get("/")
        request.session = {}
        request.user = get_django_user('javerage')

        set_override_user(request, "supportticket")
        self.assertEqual(request.user.username, 'supportticket')
        self.assertEqual(get_user(request), 'supportticket')
        self.assertEqual(get_acting_user(request), 'javerage')
        self.assertEqual(get_override_user(request), 'supportticket')
        self.assertEqual(get_original_user(request), 'javerage')

    def test_clear_override(self):
        request = RequestFactory().get("/")
        request.session = {}
        request.user = get_django_user('javerage')

        set_override_user(request, "supportticket")
        clear_override(request)
        self.assertEqual(request.user.username, 'javerage')

        self.assertEqual(get_user(request), 'javerage')
        self.assertEqual(get_acting_user(request), 'javerage')
        self.assertEqual(get_override_user(request), None)
        self.assertEqual(get_original_user(request), 'javerage')

    def test_legacy(self):
        request = RequestFactory().get("/")
        request.session = {}
        request.user = get_django_user('javerage')

        get_user(request)
        set_override_user(request, "override")

        UserServiceMiddleware().process_request(request)

        self.assertEqual(UserService().get_user(), 'override')
        self.assertEqual(UserService().get_acting_user(), 'javerage')
        self.assertEqual(UserService().get_original_user(), 'javerage')
        self.assertEqual(UserService().get_override_user(), 'override')
        UserServiceMiddleware().process_response(request, None)

    def test_legacy_other_way(self):
        request = RequestFactory().get("/")
        request.session = {}
        request.user = get_django_user('javerage')

        UserServiceMiddleware().process_request(request)

        UserService().set_override_user('o2')

        self.assertEqual(get_user(request), 'o2')
        self.assertEqual(get_acting_user(request), 'javerage')
        self.assertEqual(get_override_user(request), 'o2')
        self.assertEqual(get_original_user(request), 'javerage')
        UserServiceMiddleware().process_response(request, None)
