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
"""Tests for suppressing the document byline on the ONLYOFFICE editor views."""

from onlyoffice.plone.browser.viewlets import HiddenDocumentBylineViewlet
from onlyoffice.plone.testing import ONLYOFFICE_PLONE_INTEGRATION_TESTING
from plone import api
from plone.app.layout.viewlets.interfaces import IBelowContentTitle
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter
from zope.viewlet.interfaces import IViewlet

import unittest


BYLINE_NAME = "plone.belowcontenttitle.documentbyline"


class TestDocumentBylineViewlet(unittest.TestCase):
    """The byline must be suppressed for the editor views only."""

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

    def _lookup_byline(self, view):
        manager = getMultiAdapter(
            (self.file, self.request, view),
            IBelowContentTitle,
            name="plone.belowcontenttitle",
        )
        manager.update()
        return queryMultiAdapter(
            (self.file, self.request, view, manager),
            IViewlet,
            name=BYLINE_NAME,
        )

    def test_byline_suppressed_for_editor_view(self):
        """The ONLYOFFICE editor view gets the no-op byline viewlet."""
        view = getMultiAdapter((self.file, self.request), name="onlyoffice-view")
        viewlet = self._lookup_byline(view)
        self.assertIsInstance(viewlet, HiddenDocumentBylineViewlet)
        viewlet.update()
        self.assertEqual(viewlet.render().strip(), "")

    def test_byline_not_overridden_for_non_editor_view(self):
        """A regular view does not get the no-op byline override.

        The override must be scoped to the editor views (IOnlyofficeEditorView)
        only, leaving the default byline in place everywhere else.
        """
        view = BrowserView(self.file, self.request)
        viewlet = self._lookup_byline(view)
        self.assertNotIsInstance(viewlet, HiddenDocumentBylineViewlet)
