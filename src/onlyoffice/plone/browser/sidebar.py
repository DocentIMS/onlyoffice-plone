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

from onlyoffice.plone.core import fileUtils
from plone.protect.utils import addTokenToUrl
from Products.CMFCore.interfaces import IFolderish
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from zope.security import checkPermission


class OnlyofficeSidebar(BrowserView):
    """Data for the collapsible ONLYOFFICE group rendered by collective.sidebar.

    The sidebar template (overridden via z3c.jbot) calls ``available()`` to
    decide whether to show the group and ``items()`` to list the document types
    that can be created in the current folder. Text only - the ONLYOFFICE icons
    are white and would be invisible on the light sidebar.
    """

    document_types = ("word", "cell", "slide", "form")

    def __call__(self):
        # This view is only traversed for its data methods from the sidebar
        # template; it is never rendered on its own.
        return ""

    def _add_context(self):
        # The folder new content should be created in. This mirrors what
        # collective.sidebar uses for its "Add" section, so the ONLYOFFICE group
        # shows in the same places - including the site root front page, whose
        # add context is the root folder rather than the default-page document.
        factories = getMultiAdapter(
            (self.context, self.request), name="folder_factories"
        )
        return factories.add_context()

    def available(self):
        try:
            add_context = self._add_context()
        except Exception:  # never let the sidebar widget break the page
            return False
        return bool(
            IFolderish.providedBy(add_context)
            and checkPermission("cmf.AddPortalContent", add_context)
        )

    def items(self):
        base_url = self._add_context().absolute_url()
        result = []
        for document_type in self.document_types:
            result.append(
                {
                    "title": fileUtils.getDefaultNameByType(document_type),
                    "url": addTokenToUrl(
                        f"{base_url}/onlyoffice-create?documentType={document_type}",
                        self.request,
                    ),
                }
            )
        return result
