"""Build the Docent blank templates (new.docx / new.xlsx / new.pptx).

Takes ONLYOFFICE's English blank templates from the app_data submodule and
writes Docent-styled copies to src/onlyoffice/plone/browser/docent_templates:
Docent theme colours and the Inter font in every file, plus Docent title,
heading and table styles in the Word template.

Run from the repository root after `git submodule update --init`:

    python scripts/build_docent_templates.py
"""

import os
import re
import zipfile


HERE = os.path.dirname(os.path.abspath(__file__))
BROWSER = os.path.join(HERE, "..", "src", "onlyoffice", "plone", "browser")
SOURCE = os.path.join(BROWSER, "app_data", "en")
TARGET = os.path.join(BROWSER, "docent_templates")

FONT = "Inter"

# Docent palette (medialog.docenttheme --docent-* tokens).
COLORS = [
    ("dk1", "212529"),  # ink
    ("lt1", "FFFFFF"),
    ("dk2", "1F5F6E"),  # action teal
    ("lt2", "F6F2EC"),  # warm surface
    ("accent1", "1F5F6E"),  # teal
    ("accent2", "64041F"),  # brand maroon
    ("accent3", "3A9FB5"),  # bright teal
    ("accent4", "2F9E57"),  # success green
    ("accent5", "BC8D0D"),  # warning amber
    ("accent6", "6B635C"),  # stone
    ("hlink", "1F5F6E"),
    ("folHlink", "64041F"),
]

CLR_SCHEME = (
    '<a:clrScheme name="Docent">'
    + "".join(f'<a:{k}><a:srgbClr val="{v}"/></a:{k}>' for k, v in COLORS)
    + "</a:clrScheme>"
)

FONT_SCHEME = (
    '<a:fontScheme name="Docent">'
    '<a:majorFont><a:latin typeface="{f}"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont>'
    '<a:minorFont><a:latin typeface="{f}"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont>'
    "</a:fontScheme>"
).format(f=FONT)


def docent_theme(xml):
    xml = re.sub(
        r"<a:clrScheme\b.*?</a:clrScheme>", CLR_SCHEME, xml, count=1, flags=re.S
    )
    xml = re.sub(
        r"<a:fontScheme\b.*?</a:fontScheme>", FONT_SCHEME, xml, count=1, flags=re.S
    )
    xml = re.sub(r'(<a:theme\b[^>]*\bname=")[^"]*"', r'\1Docent"', xml, count=1)
    return xml


def _heading(style_id, name, size, color, before, after, level, extra_ppr=""):
    return (
        '<w:style w:type="paragraph" w:styleId="{id}"><w:name w:val="{name}"/>'
        '<w:basedOn w:val="a"/><w:next w:val="a"/><w:uiPriority w:val="9"/><w:qFormat/>'
        '<w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="{b}" w:after="{a}"/>{x}'
        '<w:outlineLvl w:val="{lvl}"/></w:pPr>'
        '<w:rPr><w:rFonts w:asciiTheme="majorHAnsi" w:hAnsiTheme="majorHAnsi"/>'
        '<w:b/><w:bCs/><w:color w:val="{c}"/><w:sz w:val="{s}"/><w:szCs w:val="{s}"/></w:rPr>'
        "</w:style>"
    ).format(
        id=style_id,
        name=name,
        s=size,
        c=color,
        b=before,
        a=after,
        lvl=level,
        x=extra_ppr,
    )


DOCX_STYLES = (
    # Title: teal, large, with a maroon rule under it.
    '<w:style w:type="paragraph" w:styleId="DocentTitle"><w:name w:val="Title"/>'
    '<w:basedOn w:val="a"/><w:next w:val="a"/><w:uiPriority w:val="10"/><w:qFormat/>'
    '<w:pPr><w:pBdr><w:bottom w:val="single" w:sz="12" w:space="4" w:color="64041F"/></w:pBdr>'
    '<w:spacing w:after="240" w:line="240" w:lineRule="auto"/><w:contextualSpacing/></w:pPr>'
    '<w:rPr><w:rFonts w:asciiTheme="majorHAnsi" w:hAnsiTheme="majorHAnsi"/><w:b/><w:bCs/>'
    '<w:color w:val="1F5F6E"/><w:spacing w:val="-6"/><w:kern w:val="28"/>'
    '<w:sz w:val="52"/><w:szCs w:val="52"/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="DocentSubtitle"><w:name w:val="Subtitle"/>'
    '<w:basedOn w:val="a"/><w:next w:val="a"/><w:uiPriority w:val="11"/><w:qFormat/>'
    '<w:rPr><w:color w:val="7A736C"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>'
    + _heading("DocentHeading1", "heading 1", 32, "1F5F6E", 360, 120, 0)
    + _heading("DocentHeading2", "heading 2", 26, "17505D", 280, 80, 1)
    + _heading("DocentHeading3", "heading 3", 22, "212529", 240, 60, 2)
    # Docent Table: teal header row, warm banded rows, light borders.
    + '<w:style w:type="table" w:styleId="DocentTable"><w:name w:val="Docent Table"/>'
    '<w:basedOn w:val="a1"/><w:uiPriority w:val="59"/><w:qFormat/>'
    '<w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>'
    '<w:tblPr><w:tblStyleRowBandSize w:val="1"/><w:tblBorders>'
    '<w:top w:val="single" w:sz="4" w:space="0" w:color="DFD9D1"/>'
    '<w:left w:val="single" w:sz="4" w:space="0" w:color="DFD9D1"/>'
    '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="DFD9D1"/>'
    '<w:right w:val="single" w:sz="4" w:space="0" w:color="DFD9D1"/>'
    '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="DFD9D1"/>'
    '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="DFD9D1"/>'
    "</w:tblBorders></w:tblPr>"
    '<w:tblStylePr w:type="firstRow"><w:rPr><w:b/><w:bCs/><w:color w:val="FFFFFF"/></w:rPr>'
    '<w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="1F5F6E"/></w:tcPr></w:tblStylePr>'
    '<w:tblStylePr w:type="band2Horz"><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="F6F2EC"/></w:tcPr></w:tblStylePr>'
    "</w:style>"
)


def docent_docx_styles(xml):
    # Body text in Docent ink.
    xml = xml.replace(
        '<w:style w:type="paragraph" w:default="1" w:styleId="a"><w:name w:val="Normal"/><w:qFormat/></w:style>',
        '<w:style w:type="paragraph" w:default="1" w:styleId="a"><w:name w:val="Normal"/><w:qFormat/>'
        '<w:rPr><w:color w:val="212529"/></w:rPr></w:style>',
    )
    assert "DocentHeading1" not in xml
    return xml.replace("</w:styles>", DOCX_STYLES + "</w:styles>")


def docent_xlsx_styles(xml):
    return re.sub(
        r'(<font>.*?<name val=")[^"]*(")', r"\g<1>%s\2" % FONT, xml, count=1, flags=re.S
    )


def build(name, transforms):
    src = os.path.join(SOURCE, name)
    dst = os.path.join(TARGET, name)
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(
        dst, "w", zipfile.ZIP_DEFLATED
    ) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            for match, fn in transforms:
                if re.search(match, item.filename):
                    data = fn(data.decode("utf-8")).encode("utf-8")
            zout.writestr(item, data)
    print("wrote", os.path.relpath(dst))


def main():
    os.makedirs(TARGET, exist_ok=True)
    theme = (r"/theme/theme\d+\.xml$", docent_theme)
    build("new.docx", [theme, (r"^word/styles\.xml$", docent_docx_styles)])
    build("new.xlsx", [theme, (r"^xl/styles\.xml$", docent_xlsx_styles)])
    build("new.pptx", [theme])


if __name__ == "__main__":
    main()
