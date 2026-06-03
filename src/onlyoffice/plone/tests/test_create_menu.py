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
"""The 'Create with ONLYOFFICE' menu must be scoped to the add-on layer."""

from onlyoffice.plone.browser.menu import OnlyofficeCreateSubMenuItem
from onlyoffice.plone.interfaces import IOnlyofficePloneLayer
from onlyoffice.plone.testing import ONLYOFFICE_PLONE_INTEGRATION_TESTING
from plone.app.contentmenu.interfaces import IContentMenuItem
from zope.component import getGlobalSiteManager
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

import unittest


MENU_ITEM_NAME = "plone.contentmenu.onlyoffice.create"


class TestCreateMenuLayerScoped(unittest.TestCase):
    """The content menu item is registered only for IOnlyofficePloneLayer."""

    layer = ONLYOFFICE_PLONE_INTEGRATION_TESTING

    def _lookup(self, request_layer):
        gsm = getGlobalSiteManager()
        return gsm.adapters.lookup(
            (Interface, request_layer),
            IContentMenuItem,
            MENU_ITEM_NAME,
        )

    def test_registered_for_addon_layer(self):
        """With the add-on layer the menu item adapter is found."""
        factory = self._lookup(IOnlyofficePloneLayer)
        self.assertIs(factory, OnlyofficeCreateSubMenuItem)

    def test_not_registered_without_addon_layer(self):
        """A request without the add-on layer does not resolve the menu item.

        IOnlyofficePloneLayer is only applied to the request once the add-on is
        installed, so on a plain request the item is absent and the menu does
        not show up in sites where ONLYOFFICE is not installed.
        """
        self.assertIsNone(self._lookup(IDefaultBrowserLayer))
