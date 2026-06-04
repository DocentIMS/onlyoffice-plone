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
"""Tests for the editor configuration customization defaults."""

from onlyoffice.plone.browser.actions import get_config
from onlyoffice.plone.testing import ONLYOFFICE_PLONE_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.namedfile.file import NamedBlobFile
from zope.component import getMultiAdapter

import json
import unittest


class TestEditorCustomization(unittest.TestCase):
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
        self.file.file = NamedBlobFile(b"data", filename="document.docx")

    def _customization(self):
        view = getMultiAdapter((self.file, self.request), name="onlyoffice-view")
        config = json.loads(get_config(view, False))
        return config["editorConfig"]["customization"]

    def test_hidden_ui_elements(self):
        customization = self._customization()
        for option in (
            "feedback",
            "help",
            "about",
            "chat",
            "leftMenu",
            "statusBar",
            "rulers",
        ):
            self.assertFalse(
                customization[option],
                f"expected {option} to default to False (hidden)",
            )

    def test_toolbar_and_panels(self):
        customization = self._customization()
        self.assertTrue(customization["compactToolbar"])
        self.assertTrue(customization["toolbarNoTabs"])
        self.assertTrue(customization["hideRightMenu"])

    def test_saving_is_manual(self):
        customization = self._customization()
        # Autosave off + forcesave on = explicit Save button that persists to Plone.
        self.assertFalse(customization["autosave"])
        self.assertTrue(customization["forcesave"])

    def test_appearance_defaults(self):
        customization = self._customization()
        self.assertEqual(customization["uiTheme"], "theme-dark")
        self.assertEqual(customization["unit"], "inch")

    def test_goback_points_to_parent(self):
        customization = self._customization()
        self.assertEqual(
            customization["goback"]["url"], self.portal.absolute_url()
        )

    def test_docent_logo(self):
        logo = self._customization()["logo"]
        self.assertTrue(logo["image"].endswith("/docent-logo.svg"))
        self.assertTrue(logo["imageDark"].endswith("/docent-logo-dark.svg"))
        self.assertTrue(logo["url"])
