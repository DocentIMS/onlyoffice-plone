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

from plone.app.layout.viewlets.common import ViewletBase


class HiddenDocumentBylineViewlet(ViewletBase):
    """No-op replacement for the default document byline viewlet.

    Registered for the ONLYOFFICE editor views (see IOnlyofficeEditorView) so
    the byline (author and modification date) is not rendered above the
    embedded editor, where it only duplicates information already shown in the
    breadcrumb and the editor header.
    """

    def render(self):
        return ""
