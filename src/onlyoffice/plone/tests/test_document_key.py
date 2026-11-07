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
        self.revisions = []
        self.callback._saveRevision = lambda users: self.revisions.append(users)

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


class TestCallbackHistory(TestCallbackForceSave):
    """Each editing session leaves one revision, made when it ends."""

    def test_session_end_leaves_one_revision(self):
        self.callback._handleStatus(2, "http://docserver/out.docx", ["jane"])
        self.assertEqual(self.revisions, [["jane"]])

    def test_save_while_editing_makes_no_revision_yet(self):
        self.callback._handleStatus(6, "http://docserver/out.docx", ["jane"])
        self.callback._handleStatus(6, "http://docserver/out.docx", ["jane"])
        self.assertEqual(self.revisions, [])

    def test_saves_then_session_end_leave_one_revision(self):
        self.callback._handleStatus(6, "http://docserver/out.docx", ["jane"])
        self.callback._handleStatus(6, "http://docserver/out.docx", ["jane"])
        self.callback._handleStatus(2, "http://docserver/out.docx", ["jane"])
        self.assertEqual(len(self.revisions), 1)

    def test_save_then_close_unchanged_leaves_a_revision(self):
        self.callback._handleStatus(6, "http://docserver/out.docx", ["jane"])
        self.callback._handleStatus(4, None, ["jane"])
        self.assertEqual(self.revisions, [["jane"]])
        self.assertFalse(utils.sessionSaved(self.file))

    def test_close_unchanged_without_save_leaves_none(self):
        self.callback._handleStatus(4, None)
        self.assertEqual(self.revisions, [])

    def test_cancel_without_save_leaves_none(self):
        utils.markDiscard(self.file)
        self.callback._handleStatus(2, "http://docserver/out.docx", ["jane"])
        self.assertEqual(self.saved, [])
        self.assertEqual(self.revisions, [])

    def test_cancel_after_save_keeps_the_saved_revision(self):
        self.callback._handleStatus(6, "http://docserver/out.docx", ["jane"])
        utils.markDiscard(self.file)
        self.callback._handleStatus(2, "http://docserver/out.docx", ["jane"])
        self.assertEqual(self.saved, ["http://docserver/out.docx"])
        self.assertEqual(len(self.revisions), 1)

    def test_next_session_starts_clean(self):
        self.callback._handleStatus(6, "http://docserver/out.docx", ["jane"])
        self.callback._handleStatus(2, "http://docserver/out.docx", ["jane"])
        self.callback._handleStatus(4, None)
        self.assertEqual(len(self.revisions), 1)


class TestSaveRevision(unittest.TestCase):
    layer = ONLYOFFICE_PLONE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.file = api.content.create(
            container=self.portal,
            type="File",
            id="history.docx",
            title="History.docx",
        )
        self.repository = api.portal.get_tool("portal_repository")

    def _length(self):
        history = self.repository.getHistoryMetadata(self.file)
        return history.getLength(countPurged=False) if history else 0

    def test_not_versionable_saves_nothing(self):
        types = [
            t for t in self.repository.getVersionableContentTypes() if t != "File"
        ]
        self.repository.setVersionableContentTypes(types)
        self.assertFalse(utils.saveRevision(self.file, [TEST_USER_ID]))

    def test_versionable_file_gets_a_revision_naming_the_editor(self):
        types = list(self.repository.getVersionableContentTypes())
        if "File" not in types:
            self.repository.setVersionableContentTypes(types + ["File"])
        before = self._length()
        self.assertTrue(utils.saveRevision(self.file, [TEST_USER_ID]))
        self.assertEqual(self._length(), before + 1)
        history = self.repository.getHistoryMetadata(self.file)
        meta = history.retrieve(self._length() - 1)["metadata"]["sys_metadata"]
        self.assertTrue(meta["comment"].startswith("Edited in ONLYOFFICE by "))

    def test_original_is_kept_once_before_the_first_edit(self):
        types = list(self.repository.getVersionableContentTypes())
        if "File" not in types:
            self.repository.setVersionableContentTypes(types + ["File"])
        if self._length():
            self.assertFalse(utils.saveOriginalRevision(self.file))
            return
        self.assertTrue(utils.saveOriginalRevision(self.file))
        self.assertEqual(self._length(), 1)
        self.assertFalse(utils.saveOriginalRevision(self.file))
        self.assertEqual(self._length(), 1)
