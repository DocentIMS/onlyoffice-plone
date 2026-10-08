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
"""Tests for onlyoffice-open, the default view of File.

For a file it does not open in ONLYOFFICE it must render Plone's own
file_view, whose download link works. It used to render the generic
Dexterity "view", whose download link goes through
<file>/view/++widget++form.widgets.file/@@download/<name> and answers 404.
"""

from onlyoffice.plone.browser.defaultview import OnlyofficeOpen
from onlyoffice.plone.testing import ONLYOFFICE_PLONE_INTEGRATION_TESTING
from plone import api
from plone.app.contenttypes.interfaces import IPloneAppContenttypesLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.namedfile.file import NamedBlobFile
from zope.interface import alsoProvides
from zope.interface import noLongerProvides

import unittest


class TestOnlyofficeOpenFallback(unittest.TestCase):
    layer = ONLYOFFICE_PLONE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.file = api.content.create(
            container=self.portal,
            type="File",
            id="setup.exe",
            title="Installer",
        )
        self.file.file = NamedBlobFile(b"MZ", filename="setup.exe")

    def render(self):
        return OnlyofficeOpen(self.file, self.request)()

    def test_not_an_onlyoffice_file_gets_file_view(self):
        alsoProvides(self.request, IPloneAppContenttypesLayer)
        html = self.render()
        self.assertIn(self.file.absolute_url() + "/@@download/file/setup.exe", html)
        self.assertNotIn("++widget++", html)

    def test_without_file_view_it_still_renders_a_page(self):
        # Where plone.app.contenttypes' browser layer is not active,
        # file_view is not registered: the generic view is what is left.
        noLongerProvides(self.request, IPloneAppContenttypesLayer)
        html = self.render()
        self.assertIn("setup.exe", html)
        self.assertNotIn("@@download/file/setup.exe", html)
