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

PROFILE_ID = "onlyoffice.plone:default"


def upgrade_to_2(context):
    context.runImportStepFromProfile(
        PROFILE_ID.replace("default", "to_2"),
        "plone.app.registry",
    )


def add_onlyoffice_permissions(context):
    # Apply the new ONLYOFFICE view/review/edit permission role mappings on
    # existing installs.
    context.runImportStepFromProfile(PROFILE_ID, "rolemap")


def add_direct_open_setting(context):
    # Add the new "directly open" registry record on existing installs.
    context.runImportStepFromProfile(PROFILE_ID, "plone.app.registry")


def enable_direct_open_view(context):
    # Register the onlyoffice-open File default view on existing installs.
    context.runImportStepFromProfile(PROFILE_ID, "typeinfo")


def add_sidebar_actions(context):
    # Recategorize the File/Document ONLYOFFICE actions to 'object_buttons' so
    # they surface in the sidebar's Actions section, and import the actions tool.
    context.runImportStepFromProfile(PROFILE_ID, "actions")
    context.runImportStepFromProfile(PROFILE_ID, "typeinfo")


def remove_sidebar_links_actions(context):
    # Earlier 4050 added flat create links in the 'sidebar_links' action
    # category. These are replaced by the collapsible ONLYOFFICE group rendered
    # by the sidebar template override, so remove the now-redundant actions.
    from plone import api

    portal_actions = api.portal.get_tool("portal_actions")
    category = portal_actions.get("sidebar_links")
    if category is None:
        return
    for action_id in (
        "onlyoffice-create-word",
        "onlyoffice-create-cell",
        "onlyoffice-create-slide",
        "onlyoffice-create-form",
    ):
        if action_id in category.objectIds():
            category.manage_delObjects([action_id])
