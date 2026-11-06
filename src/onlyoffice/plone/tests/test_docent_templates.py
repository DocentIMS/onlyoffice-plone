"""Tests for Docent's blank document templates."""

import onlyoffice.plone.browser
import os
import unittest
import zipfile


TEMPLATES = os.path.join(
    os.path.dirname(onlyoffice.plone.browser.__file__), "docent_templates"
)

THEMES = {
    "new.docx": "word/theme/theme1.xml",
    "new.xlsx": "xl/theme/theme1.xml",
    "new.pptx": "ppt/theme/theme1.xml",
}


class TestDocentTemplates(unittest.TestCase):
    def _read(self, name, member):
        with zipfile.ZipFile(os.path.join(TEMPLATES, name)) as z:
            return z.read(member).decode("utf-8")

    def test_every_template_has_the_docent_theme(self):
        for name, member in THEMES.items():
            theme = self._read(name, member)
            self.assertIn('<a:clrScheme name="Docent">', theme, name)
            self.assertIn('<a:accent1><a:srgbClr val="1F5F6E"/>', theme, name)
            self.assertIn('<a:latin typeface="Inter"/>', theme, name)

    def test_word_template_has_docent_styles(self):
        styles = self._read("new.docx", "word/styles.xml")
        for style in ("Title", "heading 1", "heading 2", "heading 3", "Docent Table"):
            self.assertIn('<w:name w:val="%s"/>' % style, styles)

    def test_spreadsheet_body_font_is_inter(self):
        self.assertIn('<name val="Inter"/>', self._read("new.xlsx", "xl/styles.xml"))
