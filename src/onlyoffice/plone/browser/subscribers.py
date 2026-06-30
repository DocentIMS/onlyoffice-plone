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

from onlyoffice.plone.core import utils

# Field names that hold editable document content.
CONTENT_FIELDS = {"file", "image"}


def _content_field_changed(event):
    # Only react when we can positively identify that a content field changed.
    # Metadata-only edits (e.g. title) must keep the key stable so they do not
    # split an active co-editing session.
    for description in getattr(event, "descriptions", None) or ():
        attributes = set(getattr(description, "attributes", ()) or ())
        if attributes & CONTENT_FIELDS:
            return True
    return False


def reset_document_key_on_content_change(obj, event):
    """Give the document a new ONLYOFFICE key when its file is replaced.

    Fired on ObjectModifiedEvent. When the content is changed outside the
    editor (e.g. via the Plone edit form), the document is a new version and
    must get a new key; the in-editor save path resets the key itself.
    """
    if _content_field_changed(event):
        utils.resetDocumentKey(obj)
