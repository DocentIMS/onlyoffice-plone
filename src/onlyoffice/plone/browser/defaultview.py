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
from onlyoffice.plone.core import utils
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter


class OnlyofficeOpen(BrowserView):
    """Default view for File that, when the "directly open" setting is on and
    the file is a format ONLYOFFICE manages, redirects to the ONLYOFFICE editor
    in the highest mode the user is allowed (edit -> review -> view).

    In every other case - the setting is off, the file is not an
    ONLYOFFICE-managed format, or the user has no ONLYOFFICE access - it renders
    the standard Plone file view unchanged.
    """

    def _onlyofficeTarget(self):
        context = self.context

        if not utils.isDirectOpenEnabled() or not fileUtils.canView(context):
            return None

        if fileUtils.canEdit(context) and utils.userCanEdit(context):
            return "onlyoffice-edit"
        if fileUtils.canEdit(context) and utils.userCanReview(context):
            return "onlyoffice-review"
        if utils.userCanView(context):
            return "onlyoffice-view"

        return None

    def __call__(self):
        target = self._onlyofficeTarget()
        if target:
            self.request.response.redirect(f"{self.context.absolute_url()}/{target}")
            return ""

        # Fall back to the standard Plone file view, rendered inline (no
        # redirect, no behaviour change when the setting is off or the file is
        # not OO-managed). That is file_view, plone.app.contenttypes' File
        # view - not "view", the generic Dexterity display form: its download
        # link is <file>/view/++widget++form.widgets.file/@@download/<name>,
        # and "view" leads back here, to a page that is not a form, so the
        # link answers 404. file_view links to <file>/@@download/file/<name>.
        # It is registered on plone.app.contenttypes' browser layer, so where
        # that layer is not active it does not exist; keep "view" then.
        view = queryMultiAdapter((self.context, self.request), name="file_view")
        if view is None:
            view = getMultiAdapter((self.context, self.request), name="view")
        return view()
