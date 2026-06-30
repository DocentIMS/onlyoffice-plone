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
"""Tests for the ONLYOFFICE view/review/edit permissions."""

from onlyoffice.plone import permissions as oo_permissions
from onlyoffice.plone.core import utils
from onlyoffice.plone.testing import ONLYOFFICE_PLONE_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.namedfile.file import NamedBlobFile

import unittest


class TestOnlyofficePermissions(unittest.TestCase):
    layer = ONLYOFFICE_PLONE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.file = api.content.create(
            container=self.portal,
            type="File",
            id="document.docx",
            title="Document",
        )
        self.file.file = NamedBlobFile(b"data", filename="document.docx")

    def test_permissions_are_registered(self):
        possible = self.file.possible_permissions()
        for perm in (
            oo_permissions.ViewDocument,
            oo_permissions.ReviewDocument,
            oo_permissions.EditDocument,
        ):
            self.assertIn(perm, possible, f"{perm} should be registered")

    def test_manager_has_all_onlyoffice_access(self):
        self.assertTrue(utils.userCanView(self.file))
        self.assertTrue(utils.userCanReview(self.file))
        self.assertTrue(utils.userCanEdit(self.file))
