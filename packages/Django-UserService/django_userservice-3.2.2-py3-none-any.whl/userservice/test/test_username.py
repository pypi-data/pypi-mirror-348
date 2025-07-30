# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import TestCase
from django.conf import settings
from userservice.username import get_uid


class TestUserName(TestCase):

    def test_default(self):
        self.assertIsNone(get_uid(None))
        self.assertEqual(get_uid("dummy"), "dummy")
        remote_user_name = "dummy@uw.edu"
        self.assertEqual(get_uid(remote_user_name), remote_user_name)

    def test_uwnetid(self):
        with self.settings(REMOTE_USER_FORMAT='uwnetid'):
            self.assertIsNone(get_uid(None))
            self.assertEqual(get_uid("dummy"), "dummy")
            self.assertEqual(get_uid("dummy@uw.edu"), "dummy")
            self.assertEqual(get_uid("dummy@washington.edu"), "dummy")
