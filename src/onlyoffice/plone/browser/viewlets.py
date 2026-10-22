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


# The "Changes saved" note (2026-10-21). The editor page (templates/view.pt)
# leaves {name, saved} in sessionStorage under NOTE_KEY when someone leaves
# it after editing - by Save & Close, the breadcrumb or anything else - and
# whichever page comes next shows the note once, in the bottom right corner,
# for four seconds. Save & Close has stored the document by then: "Changes
# saved". Any other way out leaves the document server to write it back a
# few seconds later: "Changes are being saved" (2026-10-22). A plain string
# (an editor page from before that) reads as saved. "Don't show this again"
# is kept per browser in localStorage under HIDE_KEY.
NOTE_KEY = "docentChangesSaved"
HIDE_KEY = "docentHideChangesSaved"

CHANGES_SAVED_NOTE = """<style>
.oo-saved-note{position:fixed;right:18px;bottom:18px;z-index:100001;width:320px;
background:#fff;border:1px solid #DFD9D1;border-left:4px solid #1F5F6E;border-radius:6px;
box-shadow:0 8px 26px rgba(0,0,0,.16);padding:12px 38px 0 14px;font-size:13px;color:#212529;
overflow:hidden;font-family:inherit}
.oo-saved-note b{display:block;font-size:14px}
.oo-saved-note small{display:block;color:#5B5650;margin-top:2px;overflow:hidden;
text-overflow:ellipsis;white-space:nowrap}
.oo-saved-note label{display:flex;align-items:center;gap:6px;margin:10px 0 10px;
font-size:12px;color:#5B5650;cursor:pointer}
.oo-saved-note button{position:absolute;top:6px;right:6px;width:28px;height:28px;border:0;
background:transparent;font-size:18px;line-height:1;color:#5B5650;cursor:pointer}
.oo-saved-note i{display:block;height:3px;margin:0 -38px 0 -14px;background:#1F5F6E;
animation:oo-saved-run 4s linear forwards}
@keyframes oo-saved-run{from{width:100%}to{width:0}}
</style>
<script>
(function () {
  var name, saved = true, raw;
  try {
    raw = window.sessionStorage.getItem("__NOTE_KEY__");
    if (raw === null) { return; }
    name = raw;
    try {
      var data = JSON.parse(raw);
      if (data && typeof data === "object") {
        name = data.name || "";
        saved = !!data.saved;
      }
    } catch (e) { /* the old plain name */ }
    window.sessionStorage.removeItem("__NOTE_KEY__");
    if (window.localStorage.getItem("__HIDE_KEY__") === "1") { return; }
  } catch (e) { return; }
  function show() {
    var note = document.createElement("div");
    note.className = "oo-saved-note";
    note.setAttribute("role", "status");
    note.innerHTML = '<b></b><small></small>'
      + '<label><input type="checkbox"> Don&#8217;t show this again</label>'
      + '<button type="button" aria-label="Dismiss" title="Dismiss">&times;</button><i></i>';
    note.querySelector("b").textContent =
      saved ? "Changes saved" : "Changes are being saved";
    note.querySelector("small").textContent = saved ? name
      : name + " \u2014 ONLYOFFICE is writing them to Docent.";
    function close() { if (note.parentNode) { note.parentNode.removeChild(note); } }
    note.querySelector("button").addEventListener("click", close);
    note.querySelector("input").addEventListener("change", function (event) {
      try {
        if (event.target.checked) { window.localStorage.setItem("__HIDE_KEY__", "1"); }
        else { window.localStorage.removeItem("__HIDE_KEY__"); }
      } catch (e) { /* nothing to remember it in */ }
    });
    document.body.appendChild(note);
    window.setTimeout(close, 4000);
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", show);
  } else {
    show();
  }
})();
</script>""".replace(
    "__NOTE_KEY__", NOTE_KEY
).replace(
    "__HIDE_KEY__", HIDE_KEY
)


class ChangesSavedNoteViewlet(ViewletBase):
    """Shows "Changes saved" once, on the page reached after leaving an
    edited document in the ONLYOFFICE editor. Renders the same small style and
    script on every page; the script does nothing unless the editor left its
    note in sessionStorage."""

    def render(self):
        return CHANGES_SAVED_NOTE
