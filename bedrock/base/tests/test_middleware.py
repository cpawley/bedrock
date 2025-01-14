# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from urllib.parse import urlencode

from django.test import RequestFactory, TestCase
from django.test.utils import override_settings

from bedrock.base.middleware import LocaleURLMiddleware


@override_settings(DEV=True)
class TestLocaleURLMiddleware(TestCase):
    def setUp(self):
        self.rf = RequestFactory()
        self.middleware = LocaleURLMiddleware()

    @override_settings(DEV_LANGUAGES=("de", "fr"))
    def test_redirects_to_correct_language(self):
        """Should redirect to lang prefixed url."""
        path = "/the/dude/"
        req = self.rf.get(path, HTTP_ACCEPT_LANGUAGE="de")
        resp = self.middleware.process_request(req)
        self.assertEqual(resp["Location"], "/de" + path)

    @override_settings(DEV_LANGUAGES=("es", "fr"), LANGUAGE_CODE="en-US")
    def test_redirects_to_default_language(self):
        """Should redirect to default lang if not in settings."""
        path = "/the/dude/"
        req = self.rf.get(path, HTTP_ACCEPT_LANGUAGE="de")
        resp = self.middleware.process_request(req)
        self.assertEqual(resp["Location"], "/en-US" + path)

    @override_settings(DEV_LANGUAGES=("de", "fr"))
    def test_redirects_to_correct_language_despite_unicode_errors(self):
        """Should redirect to lang prefixed url, stripping invalid chars."""
        path = "/the/dude/"
        corrupt_querystring = "?" + urlencode({b"a\xa4\x91b\xa4\x91i\xc0de": "s"})
        corrected_querystring = "?abide=s"
        req = self.rf.get(path + corrupt_querystring, HTTP_ACCEPT_LANGUAGE="de")
        resp = self.middleware.process_request(req)
        self.assertEqual(resp["Location"], "/de" + path + corrected_querystring)
