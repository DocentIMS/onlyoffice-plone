# Change Log

## Unreleased (DocentIMS fork)
Changes maintained on the DocentIMS fork on top of upstream ONLYOFFICE 4.1.0.
## Fixed
- getFileExt no longer crashes when a content item's file field is missing, None (required setting disabled), or empty; now works for any content type that has a file field
- stabilized ONLYOFFICE document key generation and added force-save handling
## Changed
- hide the redundant Plone page title and byline (author/date) in the editor view, via a content-type-conditional viewlet and slot override
- hide the ONLYOFFICE "Feedback & Support" icon in the editor
- hide the left/right panels, status bar and rulers by default in the editor
- hide ONLYOFFICE menu entries when the add-on is not installed
- editor now fills the browser window down to the bottom instead of a fixed 600px height
## Added
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