# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


import re


def is_email(username):
    err_msg = ("No override user supplied, please enter a user to override "
               "as in the format of an email address")
    if len(username) > 0:
        match = re.match(r'[^@]+@[^@]+\.[^@]+', username)
        if not match:
            err_msg = "Override user must be an email address.  You entered: "
        else:
            err_msg = None
    return err_msg
