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

"""ONLYOFFICE-specific permissions.

These let administrators control who may open a document in the ONLYOFFICE
editor for view / review / edit independently of the generic Plone rights.
They are checked *in addition to* the corresponding Plone permission (View /
Review portal content / Modify portal content), so they act as an extra gate
on top of normal Plone access.

The default role mappings below mirror the roles that already hold the matching
Plone right, so installing the add-on does not change existing behaviour; admins
then narrow access by removing roles from these permissions (site-wide via the
ZMI Security tab, or per folder).
"""

from AccessControl.Permission import addPermission


ViewDocument = "ONLYOFFICE: View document"
ReviewDocument = "ONLYOFFICE: Review document"
EditDocument = "ONLYOFFICE: Edit document"

addPermission(
    ViewDocument,
    (
        "Manager",
        "Site Administrator",
        "Owner",
        "Editor",
        "Contributor",
        "Reviewer",
        "Reader",
    ),
)
addPermission(
    ReviewDocument,
    ("Manager", "Site Administrator", "Reviewer"),
)
addPermission(
    EditDocument,
    ("Manager", "Site Administrator", "Owner", "Editor"),
)
