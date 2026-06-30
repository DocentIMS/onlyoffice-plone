#
# (c) Copyright Ascensio System SIA 2026
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# -*- coding: utf-8 -*-
"""Tests for the stable document key and force-save handling."""

from onlyoffice.plone.browser.api import Callback
from onlyoffice.plone.core import utils
from onlyoffice.plone.testing import ONLYOFFICE_PLONE_INTEGRATION_TESTING
from plone import api
from plone.app.contenttypes.interfaces import IFile
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.lifecycleevent import Attributes
from zope.lifecycleevent import modified

import re
import unittest

# Characters ONLYOFFICE permits in a document key, max length 128.
KEY_RE = re.compile(r"^[0-9A-Za-z._=-]{1,128}$")


class TestDocumentKey(unittest.TestCase):
    layer = ONLYOFFICE_PLONE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.file = api.content.create(
            container=self.portal,
            type="File",
            id="document.docx",
            title="Document.docx",
        )

    def test_key_is_stable_across_calls(self):
        self.assertEqual(
            utils.getDocumentKey(self.file), utils.getDocumentKey(self.file)
        )

    def test_key_matches_onlyoffice_constraints(self):
        self.assertRegex(utils.getDocumentKey(self.file), KEY_RE)

    def test_reset_issues_a_new_key(self):
        before = utils.getDocumentKey(self.file)
        after = utils.resetDocumentKey(self.file)
        self.assertNotEqual(before, after)
        self.assertEqual(utils.getDocumentKey(self.file), after)
        self.assertRegex(after, KEY_RE)

    def test_metadata_change_keeps_key(self):
        before = utils.getDocumentKey(self.file)
        modified(self.file, Attributes(IFile, "title"))
        self.assertEqual(utils.getDocumentKey(self.file), before)

    def test_content_change_resets_key(self):
        before = utils.getDocumentKey(self.file)
        modified(self.file, Attributes(IFile, "file"))
        self.assertNotEqual(utils.getDocumentKey(self.file), before)


class TestCallbackForceSave(unittest.TestCase):
    layer = ONLYOFFICE_PLONE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.file = api.content.create(
            container=self.portal,
            type="File",
            id="document.docx",
            title="Document.docx",
        )
        self.callback = Callback(self.file, self.request)
        # Avoid hitting the (non-existent) Document Server during the test.
        self.saved = []
        self.callback._save = lambda url: self.saved.append(url)

    def test_force_save_persists_but_keeps_key(self):
        before = utils.getDocumentKey(self.file)
        self.callback._handleStatus(6, "http://docserver/out.docx")
        self.assertEqual(self.saved, ["http://docserver/out.docx"])
        self.assertEqual(utils.getDocumentKey(self.file), before)

    def test_final_save_persists_and_resets_key(self):
        before = utils.getDocumentKey(self.file)
        self.callback._handleStatus(2, "http://docserver/out.docx")
        self.assertEqual(self.saved, ["http://docserver/out.docx"])
        self.assertNotEqual(utils.getDocumentKey(self.file), before)

    def test_closed_without_changes_is_a_noop(self):
        before = utils.getDocumentKey(self.file)
        self.callback._handleStatus(4, None)
        self.assertEqual(self.saved, [])
        self.assertEqual(utils.getDocumentKey(self.file), before)
