# ONLYOFFICE addon for Plone

This addon allows users to edit office documents within [Plone](https://plone.org/) using [ONLYOFFICE Docs](https://www.onlyoffice.com/docs).

<p align="center">
  <a href="https://www.onlyoffice.com/office-for-plone">
    <img width="800" src="https://static-site.onlyoffice.com/public/images/templates/office-for-plone/hero/screen1@2x.png" alt="ONLYOFFICE for Plone">
  </a>
</p>

## Features ✨

The addon allows to:

* Create and edit text documents, spreadsheets, and presentations.
* Share documents with other users.
* Co-edit documents in real-time: use two co-editing modes (Fast and Strict), Track Changes, comments, and built-in chat.

### Supported file formats 📁

| Action                         | Formats                                                                                                                                                                                                                                     |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Editing**                    | DOCX, XLSX, PPTX, PDF                                                                                                                                                                                                                       |
| **Viewing**                    | DJVU, DOC, DOCM, DOCX, DOT, DOTM, DOTX, EPUB, FB2, FODT, HTML, MHT, ODT, OTT, OXPS, PDF, RTF, TXT, XPS, XML, CSV, FODS, ODS, OTS, XLS, XLSB, XLSM, XLSX, XLT, XLTM, XLTX, FODP, ODP, OTP, POT, POTM, POTX, PPS, PPSM, PPSX, PPT, PPTM, PPTX |
| **Convert (Download as)**      | DOC, DOCM, DOCX, DOT, DOTM, DOTX, EPUB, FB2, FODT, HTML, MHT, ODT, OTT, OXPS, PDF, RTF, XPS, XML, FODS, ODS, OTS, XLS, XLSB, XLSM, XLSX, XLT, XLTM, XLTX, FODP, ODP, OTP, POT, POTM, POTX, PPS, PPSM, PPSX, PPT, PPTM, PPTX                 |
| **Convert to Office Open XML** | DOC, DOCM, DOT, DOTM, DOTX, EPUB, FB2, FODT, HTML, MHT, ODT, OTT, OXPS, PDF, RTF, XPS, XML, FODS, ODS, OTS, XLS, XLSB, XLSM, XLT, XLTM, XLTX, FODP, ODP, OTP, POT, POTM, POTX, PPS, PPSM, PPSX, PPT, PPTM                                   |

## DocentIMS customizations 🏷️

This fork adds a number of integration and UX changes on top of upstream ONLYOFFICE 4.1.0. See [CHANGELOG.md](CHANGELOG.md) for the full list.

### Editor experience
- **Streamlined editor chrome:** the redundant Plone page title and byline (author/date) are removed above the editor; the ONLYOFFICE *Feedback & Support*, *Help*, *About* and *chat* items are hidden; left panel, status bar and rulers are hidden; the right panel is collapsed by default.
- **Compact toolbar:** single-row toolbar with the ribbon tabs flattened (`compactToolbar` + `toolbarNoTabs`).
- **Dark theme** and **inch** units by default (users can still change both in the editor).
- **Full-height editor:** the editor fills the browser window instead of a fixed 600px height.
- **"Open file location"** button returns to the file's parent folder.
- **Docent logo** (mono, with light and dark variants) replaces the ONLYOFFICE logo in the toolbar; it is plain branding and **not clickable**.
- **Tightened layout:** the empty top spacing above the editor frame is collapsed so the toolbar sits right under the Plone content separator.

### Saving
- **Manual save:** autosave to the document server is off; an active **Save** button force-saves straight to Plone on demand. The Save button greys out while there are no unsaved changes (native), and a **"File saved"** confirmation is shown after a manual save.
- Saves are a **full in-place overwrite** of the original file — no version history is piled up.

### Download
- A **Download** button exports the document exactly as it currently is in the editor (live state) in its native format, and **saves that same version back to Plone**, with an on-screen confirmation.

### Rename
- The editor's **Rename…** action updates both the Plone **Title** (without extension) and the stored **file name** (keeping the extension), without ending the editing session.

### Access control
- Dedicated permissions **ONLYOFFICE: View / Review / Edit document** gate editor access per role/group. They are checked **in addition** to the matching Plone right (View / Review portal content / Modify portal content) and are managed from the ZMI **Security** tab. Defaults mirror the roles that already hold those rights.

### Direct open
- A control-panel option, **"Directly open files associated with ONLYOFFICE"** (off by default), makes only OO-managed files (Microsoft Office, OpenDocument, PDF) open straight in the editor in the user's highest allowed mode (edit → review → view). All other files, and the off state, keep the standard Plone file view.

### Other
- File-type detection derives the extension from the content's **primary file field** rather than a field hardcoded as `file`, so any content type holding an OO-managed format is recognised (and it no longer crashes on missing/empty file fields).
- Added test coverage (byline viewlet, create menu, document key, editor config, permissions, file extension) and modernized setup tests.

## Installing ONLYOFFICE Docs

To use the addon, you need a running instance of ONLYOFFICE Docs (Document Server) accessible to both your Plone server and client browsers.

ONLYOFFICE Docs must be able to send POST callbacks to Plone for document status updates.

You can deploy either version below:

#### 🖥️ Self-hosted version

- **Community Edition (Free):** [Docker guide](https://github.com/ONLYOFFICE/Docker-DocumentServer) or [manual installation](https://helpcenter.onlyoffice.com/installation/docs-community-install-ubuntu.aspx)
- **Enterprise Edition:** [Installation guide](https://helpcenter.onlyoffice.com/docs/installation/enterprise)

Community Edition vs Enterprise Edition comparison can be found [here](#onlyoffice-docs-editions).

#### ☁️ Cloud

If you prefer not to maintain your own server, use **ONLYOFFICE Docs Cloud** which requires neither installation nor configuration.

👉 [Get started here](https://www.onlyoffice.com/docs-registration)

## Installing the addon

1. Installation instructions can be found under [Manage add-ons and packages](https://6.docs.plone.org/plone.api/addon.html).
2. To activate, go to `Site Setup` -> `Add-ons` and press the `Install` button to enable the addon.

You can also install the addon via Docker:
```
docker run -p 8080:8080 -e ADDONS="onlyoffice.plone" plone/plone-backend:6.1 start
```

> **📝 Note:** If you have a previous version (e.g., *onlyoffice.connector*), remove it before installing the new one.

## Configuring the addon ⚙️

Navigate to **Site Setup** → **Add-ons Configuration** → **ONLYOFFICE Configuration** and configure:

- Document Editing Service URL: Your ONLYOFFICE Docs endpoint
- Secret key: For JWT token signing and validation
- Internal request addresses (optional): For internal network routing

> JWT is enabled by default to protect the editors from unauthorized access. If setting a custom **Secret key**, ensure it matches the one in the ONLYOFFICE Docs [config file](https://api.onlyoffice.com/docs/docs-api/additional-api/signature/) for proper validation.

## Developing the addon

Run this command to install the addon from the local repository:
```
docker run -p 8080:8080 -e DEVELOP="/app/src/onlyoffice.plone" -v /path/to/onlyoffice.plone:/app/src/onlyoffice.plone plone/plone-backend:6.1 start
```

For more information, check [Developing packages variable](https://6.docs.plone.org/#developing-packages-variable).

## Upgrade the addon

1. Update instructions can be found under [Manage add-ons and packages](https://6.docs.plone.org/plone.api/addon.html).
2. Navigate to the Add-on screen (add `/prefs_install_products_form` to your site URL) and in the Upgrades list select **onlyoffice.plone** and click *Upgrade onlyoffice.plone*.

## How it works

The ONLYOFFICE addon follows the API documented [here](https://api.onlyoffice.com/docs/docs-api/get-started/basic-concepts/):

* User navigates to a document within Plone and selects the `ONLYOFFICE Edit` action.
* Plone prepares a JSON object for the Document Server with the following properties:
  * **url**: the URL that ONLYOFFICE Document Server uses to download the document;
  * **callbackUrl**: the URL that ONLYOFFICE Document Server informs about status of the document editing;
  * **key**: the UUID+Modified Timestamp to instruct ONLYOFFICE Document Server whether to download the document again or not;
  * **title**: the document Title (name).
* Plone constructs a page from a `.pt` template, filling in all of those values so that the client browser can load up the editor.
* The client browser makes a request for the javascript library from ONLYOFFICE Document Server and sends ONLYOFFICE Document Server the docEditor configuration with the above properties.
* Then ONLYOFFICE Document Server downloads the document from Plone and the user begins editing.
* ONLYOFFICE Document Server sends a POST request to the `callback` URL to inform Plone that a user is editing the document.
* When all users and client browsers are done with editing, they close the editing window.
* After 10 seconds of inactivity, ONLYOFFICE Document Server sends a POST to the `callback` URL letting Plone know that the clients have finished editing the document and closed it.
* Plone downloads the new version of the document, replacing the old one.

## ONLYOFFICE Docs editions

ONLYOFFICE offers different versions of its online document editors that can be deployed on your own servers.

* Community Edition 🆓 (`onlyoffice-documentserver` package)
* Enterprise Edition 🏢 (`onlyoffice-documentserver-ee` package)

The table below will help you to make the right choice.

| Pricing and licensing | Community Edition | Enterprise Edition |
| ------------- | ------------- | ------------- |
| | [Get it now](https://www.onlyoffice.com/download-community?utm_source=github&utm_medium=cpc&utm_campaign=GitHubPlone#docs-community)  | [Start Free Trial](https://www.onlyoffice.com/download?utm_source=github&utm_medium=cpc&utm_campaign=GitHubPlone#docs-enterprise)  |
| Cost  | FREE  | [Go to the pricing page](https://www.onlyoffice.com/docs-enterprise-prices?utm_source=github&utm_medium=cpc&utm_campaign=GitHubPlone)  |
| Number of users | up to 20 recommended | As in chosen pricing plan |
| License | GNU AGPL v.3 | Proprietary |
| **Support** | **Community Edition** | **Enterprise Edition** |
| Documentation | [Help Center](https://helpcenter.onlyoffice.com/docs/installation/community) | [Help Center](https://helpcenter.onlyoffice.com/docs/installation/enterprise) |
| Standard support | [GitHub](https://github.com/ONLYOFFICE/DocumentServer/issues) or [Community](https://community.onlyoffice.com/) | 1 or 3 years support included |
| Premium support | [Contact us](mailto:sales@onlyoffice.com) | [Contact us](mailto:sales@onlyoffice.com) |
| **Services** | **Community Edition** | **Enterprise Edition** |
| Conversion Service                | + | + |
| Live Viewer                       | + | + |
| Document Builder Service          | - | - |
| Automation API                    | - | - |
| **Interface** | **Community Edition** | **Enterprise Edition** |
| Tabbed interface                  | + | + |
| Dark theme                        | + | + |
| 125%, 150%, 175%, 200% scaling    | + | + |
| White Label                       | - | - |
| Integrated test example (node.js) | + | + |
| Admin Panel                       | - | + |
| Mobile web editors                | - | +* |
| **Plugins & Macros** | **Community Edition** | **Enterprise Edition** |
| Plugins                           | + | + |
| Macros                            | + | + |
| **Collaborative capabilities** | **Community Edition** | **Enterprise Edition** |
| Two co-editing modes              | + | + |
| Comments                          | + | + |
| Built-in chat                     | + | + |
| Review and tracking changes       | + | + |
| Display modes of tracking changes | + | + |
| Version history                   | + | + |
| **Document Editor features** | **Community Edition** | **Enterprise Edition** |
| Font and paragraph formatting   | + | + |
| Object insertion                | + | + |
| Adding Content control          | + | + |
| Editing Content control         | + | + |
| Layout tools                    | + | + |
| Table of contents               | + | + |
| Navigation panel                | + | + |
| Mail Merge                      | + | + |
| Comparing documents             | + | + |
| Multipage View                  | + | + |
| **Spreadsheet Editor features** | **Community Edition** | **Enterprise Edition** |
| Font and paragraph formatting   | + | + |
| Object insertion                | + | + |
| Functions, formulas, equations  | + | + |
| Table templates                 | + | + |
| Pivot tables                    | + | + |
| Data validation                 | + | + |
| Conditional formatting          | + | + |
| Sparklines                      | + | + |
| Sheet Views                     | + | + |
| Solver                          | + | + |
| **Presentation Editor features** | **Community Edition** | **Enterprise Edition** |
| Font and paragraph formatting   | + | + |
| Object insertion                | + | + |
| Transitions                     | + | + |
| Animations                      | + | + |
| Presenter mode                  | + | + |
| Notes                           | + | + |
| Slide Master                    | + | + |
| **Form creator features** | **Community Edition** | **Enterprise Edition** |
| Adding form fields              | + | + |
| Form preview                    | + | + |
| Saving as PDF                   | + | + |
| Role-matching colors for fields | + | + |
| **PDF Editor features**      | **Community Edition** | **Enterprise Edition** |
| Text editing and co-editing                                | + | + |
| Work with pages (adding, deleting, rotating)               | + | + |
| Inserting objects (shapes, images, hyperlinks, etc.)       | + | + |
| Text annotations (highlight, underline, cross out, stamps) | + | + |
| Redact                          | + | + |
| Comments                        | + | + |
| Freehand drawings               | + | + |
| Form filling                    | + | + |
| | [Get it now](https://www.onlyoffice.com/download-community?utm_source=github&utm_medium=cpc&utm_campaign=GitHubPlone#docs-community)  | [Start Free Trial](https://www.onlyoffice.com/download?utm_source=github&utm_medium=cpc&utm_campaign=GitHubPlone#docs-enterprise)  |

\* If supported by DMS.

## Need help? User Feedback and Support 💡

* **🐞 Found a bug?** Please report it by creating an [issue](https://github.com/ONLYOFFICE/onlyoffice-plone/issues).
* **❓ Have a question?** Ask our community and developers on the [ONLYOFFICE Forum](https://community.onlyoffice.com).
* **👨‍💻 Need help for developers?** Check our [API documentation](https://api.onlyoffice.com).