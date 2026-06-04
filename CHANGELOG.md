# Change Log

## Unreleased (DocentIMS fork)
Changes maintained on the DocentIMS fork on top of upstream ONLYOFFICE 4.1.0.
## Fixed
- getFileExt now derives the document extension from the actual stored file via the content's primary field (not a field hardcoded as "file"), so any content type holding an ONLYOFFICE-managed format (.docx, .xlsx, .pptx, ...) is recognised; still safe when the file field is missing, None, or empty
- stabilized ONLYOFFICE document key generation and added force-save handling
## Changed
- editor customization: compact single-row toolbar (no ribbon tabs), dark theme, inch units, right panel collapsed by default, Help/About/chat/Feedback hidden, autosave off with manual force-save Save button, a "back to folder" button that returns to the file's parent folder, and the Docent logo (mono, light/dark variants) in place of the ONLYOFFICE toolbar logo
- hide the redundant Plone page title and byline (author/date) in the editor view, via a content-type-conditional viewlet and slot override
- hide the ONLYOFFICE "Feedback & Support" icon in the editor
- hide the left/right panels, status bar and rulers by default in the editor
- hide ONLYOFFICE menu entries when the add-on is not installed
- editor now fills the browser window down to the bottom instead of a fixed 600px height
## Added
- "Directly open files associated with ONLYOFFICE" control-panel setting (off by default): when on, only OO-managed files (Office, ODF, PDF) open straight in the editor in the user's highest allowed mode (edit/review/view); all other files and the off state keep the standard Plone file view
- dedicated ONLYOFFICE permissions ("ONLYOFFICE: View/Review/Edit document") so access to the editor can be granted per role/group independently; checked in addition to the matching Plone right (View / Review / Modify). Defaults mirror existing roles; manage via the ZMI Security tab
- active Save button (forcesave) so users can save the document to Plone on demand mid-session; saves are a full in-place overwrite of the original file with no versions kept
- in-editor "Rename..." support: renaming the open document updates both the Plone Title (without extension) and the stored file name (keeping the extension), without ending the editing session
- "Download" button on the editor view that downloads the document as it currently is in the editor (live state) in its native MS Office format, and saves that same version back to the server so the downloaded file is also stored
- test coverage for editor byline suppression, create menu, document key and editor config
- modernized setup tests for robustness across Plone versions

## 4.1.0
## Added
- replace docxf with pdf as a form template
- ar-SA, ca-ES, da-DK, eu-ES, fi-FI, gl-ES, he-IL, hu-HU, hy-AM, id-ID, ms-MY, nb-NO, ro-RO, si-LK, sl-SI, sq-AL, sr-Cyrl-RS, sr-Latn-RS, tr-TR, ur-PK and zh-TW empty file templates
- support for plone 6.1
- document formats submodule
- jwt lifetime
- update demo document server url
- shardkey in querystring

## 4.0.0
## Added
- support for plone 6

## 3.0.0
## Added
- download as
- documents conversion
- connection to a demo document server
- settings validation
- mail merge from storage
- compare file from storage
- insert image from storage
- advanced server settings for specifying internal addresses

## Changed
- parameter document.title for editor from file object title
- document server v6.0 and earlier is no longer supported

## 2.1.1
## Fixed
- issue with packaging

## 2.1.0
## Added
- support docxf and oform formats
- create blank docxf from creation menu
- "save as" in editor

## 2.0.0
## Added
 - JWT support
## Fixed
 - Issue when files inside unpublished folders couldn't be edited

## 1.0.0
## Added
 - Edit option for DOCX, XLSX, PPTX.
 - View template for documents
 - Configuration page
 - Translations for BR, CZ, DE, EN, ES, FR, IT, JP, NL, RU, ZH