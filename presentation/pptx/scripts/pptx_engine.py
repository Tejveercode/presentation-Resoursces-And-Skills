#!/usr/bin/env python3
"""pptx_engine.py — PRIMARY PPTX generation library (python-pptx).

Builds a fully editable academic deck from a JSON deck spec:
editable text frames, tables, native shapes + connectors (diagrams),
speaker notes, status badges, slide numbering, one academic theme.

Public API:
    build_deck(spec: dict, theme: dict, out_path: str) -> str
    load_json(path) -> (data)

This library is deliberately dependency-light: python-pptx only.
"""
import json
import os

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

SLIDE_TYPES = {"title", "section", "bullets", "two_column", "table", "image", "diagram"}

# Badge color routing (exact ledger wording should be used; keyword fallback)
def _badge_color(text, theme):
    t = (text or "").lower()
    if "implement" in t and "partial" not in t and "planned" not in t and "not " not in t:
        return theme["colors"]["ok"]
    if "unknown" in t or "not verified" in t or "not implemented" in t:
        return theme["colors"]["bad"]
    return theme["colors"]["warn"]


def _rgb(hexstr):
    if isinstance(hexstr, RGBColor):  # already an RGBColor (e.g. white on section band)
        return hexstr
    hexstr = str(hexstr).lstrip("#")
    return RGBColor(int(hexstr[0:2], 16), int(hexstr[2:4], 16), int(hexstr[4:6], 16))


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _new_slide(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])  # blank


def _textbox(slide, x, y, w, h, anchor=None):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    if anchor is not None:
        tf.vertical_anchor = anchor
    return tf


def _para(tf, text, size, bold=False, color=None, font=None, align=PP_ALIGN.LEFT,
          level=0, first=False, italic=False, space_after=4):
    p = tf.paragraphs[0] if first and not tf.paragraphs[0].runs else tf.add_paragraph()
    p.alignment = align
    p.level = level
    p.space_after = Pt(space_after)
    run = p.add_run()
    run.text = text
    f = run.font
    f.size = Pt(size)
    f.bold = bold
    f.italic = italic
    f.name = font
    if color:
        f.color.rgb = _rgb(color)
    return p


def _fill_rect(slide, x, y, w, h, color, kind=MSO_SHAPE.RECTANGLE, line_color=None, line_w=None):
    shp = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.fill.solid()
    shp.fill.fore_color.rgb = _rgb(color)
    if line_color:
        shp.line.color.rgb = _rgb(line_color)
        shp.line.width = Pt(line_w or 1.0)
    else:
        shp.line.fill.background()
    shp.shadow.inherit = False
    return shp


def _badge(slide, text, theme):
    if not text:
        return
    color = _badge_color(text, theme)
    shp = _fill_rect(slide, 9.1, 0.42, 3.6, 0.42, color, kind=MSO_SHAPE.ROUNDED_RECTANGLE)
    tf = shp.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = text
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.name = theme["fonts"]["body"]
    run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)


def _h1(slide, text, theme, y=0.42):
    tf = _textbox(slide, theme["margins_in"]["left"], y, 8.3, 0.9)
    _para(tf, text, theme["sizes_pt"]["h1"], bold=True, color=theme["colors"]["primary"],
          font=theme["fonts"]["heading"], first=True)
    _fill_rect(slide, theme["margins_in"]["left"], y + 0.78, 12.13, 0.022, theme["colors"]["line"])


def _footer(slide, theme, project, idx, total):
    m = theme["margins_in"]
    if theme["footer"]["show_project"] and project:
        tf = _textbox(slide, m["left"], 7.08, 6.0, 0.32)
        _para(tf, project, theme["sizes_pt"]["small"], color=theme["colors"]["muted"],
              font=theme["fonts"]["body"], first=True)
    if theme["footer"]["show_slide_number"]:
        tf = _textbox(slide, 11.9, 7.08, 0.85, 0.32)
        _para(tf, f"{idx} / {total}", theme["sizes_pt"]["small"], color=theme["colors"]["muted"],
              font=theme["fonts"]["body"], align=PP_ALIGN.RIGHT, first=True)


def _notes(slide, text):
    if text:
        slide.notes_slide.notes_text_frame.text = str(text)


def _slide_title(prs, s, theme):
    slide = _new_slide(prs)
    _fill_rect(slide, 0, 0, theme["canvas"]["width_in"], theme["canvas"]["height_in"],
               theme["colors"]["panel"])
    _fill_rect(slide, 0, 4.9, theme["canvas"]["width_in"], 0.06, theme["colors"]["accent"])
    tf = _textbox(slide, 1.0, 2.5, 11.3, 1.8)
    _para(tf, s.get("title", ""), theme["sizes_pt"]["title"], bold=True,
          color=theme["colors"]["primary"], font=theme["fonts"]["heading"], first=True)
    if s.get("subtitle"):
        _para(tf, s["subtitle"], 20, color=theme["colors"]["ink"], font=theme["fonts"]["body"])
    if s.get("meta"):
        tf2 = _textbox(slide, 1.0, 5.15, 11.3, 1.4)
        for i, line in enumerate(s["meta"]):
            _para(tf2, line, 14, color=theme["colors"]["muted"], font=theme["fonts"]["body"],
                  first=(i == 0))
    _notes(slide, s.get("notes"))
    return slide


def _slide_section(prs, s, theme):
    slide = _new_slide(prs)
    _fill_rect(slide, 0, 0, theme["canvas"]["width_in"], theme["canvas"]["height_in"],
               theme["colors"]["primary"])
    tf = _textbox(slide, 1.0, 2.7, 11.3, 0.6)
    _para(tf, s.get("phase", ""), 18, bold=True, color=theme["colors"]["panel"],
          font=theme["fonts"]["body"], first=True)
    tf2 = _textbox(slide, 1.0, 3.3, 11.3, 1.4)
    _para(tf2, s.get("title", ""), theme["sizes_pt"]["title"], bold=True,
          color=RGBColor(0xFF, 0xFF, 0xFF), font=theme["fonts"]["heading"], first=True)
    _notes(slide, s.get("notes"))
    return slide


def _bullets_into(tf, items, theme, first=True):
    body = theme["sizes_pt"]["body"]
    for i, item in enumerate(items):
        if isinstance(item, str):
            item = {"text": item, "level": 0}
        text = item.get("text", "")
        level = int(item.get("level", 0))
        prefix = "" if item.get("no_bullet") else ("• " if level == 0 else "– ")
        _para(tf, prefix + text, body - level * 2, bold=item.get("bold", False),
              color=theme["colors"]["ink"], font=theme["fonts"]["body"], level=level,
              first=(first and i == 0), space_after=6)


def _slide_bullets(prs, s, theme):
    slide = _new_slide(prs)
    _h1(slide, s.get("title", ""), theme)
    tf = _textbox(slide, theme["margins_in"]["left"], 1.5, 12.13, 5.4)
    _bullets_into(tf, s.get("bullets", []), theme)
    _badge(slide, s.get("badge"), theme)
    _notes(slide, s.get("notes"))
    return slide


def _slide_two_column(prs, s, theme):
    slide = _new_slide(prs)
    _h1(slide, s.get("title", ""), theme)
    col_w = 5.85
    for i, (head, items, x) in enumerate([
        (s.get("left_heading", ""), s.get("left_bullets", []), theme["margins_in"]["left"]),
        (s.get("right_heading", ""), s.get("right_bullets", []), theme["margins_in"]["left"] + col_w + 0.45),
    ]):
        panel = _fill_rect(slide, x - 0.15, 1.45, col_w + 0.3, 5.35, theme["colors"]["panel"])
        panel.line.color.rgb = _rgb(theme["colors"]["line"])
        tf = _textbox(slide, x, 1.6, col_w, 5.0)
        if head:
            _para(tf, head, 18, bold=True, color=theme["colors"]["primary"],
                  font=theme["fonts"]["heading"], first=True)
        _bullets_into(tf, items, theme, first=not head)
    _badge(slide, s.get("badge"), theme)
    _notes(slide, s.get("notes"))
    return slide


def _slide_table(prs, s, theme):
    slide = _new_slide(prs)
    _h1(slide, s.get("title", ""), theme)
    cols = s.get("columns", [])
    rows = s.get("rows", [])
    if not cols or not rows:
        raise ValueError("table slide requires 'columns' and 'rows'")
    width = s.get("width", 12.13)
    x = theme["margins_in"]["left"]
    y = 1.6
    height = min(0.55 * (len(rows) + 1), 5.2)
    gfx = slide.shapes.add_table(len(rows) + 1, len(cols), Inches(x), Inches(y),
                                 Inches(width), Inches(height))
    table = gfx.table
    col_widths = s.get("col_widths")
    if col_widths and len(col_widths) == len(cols):
        total = sum(col_widths)
        for i, cw in enumerate(col_widths):
            table.columns[i].width = Inches(width * cw / total)
    for c, name in enumerate(cols):
        cell = table.cell(0, c)
        cell.text = str(name)
        pr = cell.text_frame.paragraphs[0]
        pr.runs[0].font.bold = True
        pr.runs[0].font.size = Pt(theme["sizes_pt"]["body"])
        pr.runs[0].font.name = theme["fonts"]["body"]
        pr.runs[0].font.color.rgb = _rgb("FFFFFF")
        cell.fill.solid()
        cell.fill.fore_color.rgb = _rgb(theme["colors"]["primary"])
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            cell = table.cell(r + 1, c)
            cell.text = str(val)
            para = cell.text_frame.paragraphs[0]
            if para.runs:
                para.runs[0].font.size = Pt(theme["sizes_pt"]["body"])
                para.runs[0].font.name = theme["fonts"]["body"]
                para.runs[0].font.color.rgb = _rgb(theme["colors"]["ink"])
            cell.fill.solid()
            cell.fill.fore_color.rgb = _rgb("FFFFFF" if r % 2 == 0 else theme["colors"]["panel"])
    _badge(slide, s.get("badge"), theme)
    _notes(slide, s.get("notes"))
    return slide


def _slide_image(prs, s, theme):
    slide = _new_slide(prs)
    _h1(slide, s.get("title", ""), theme)
    img = s.get("image")
    if not img or not os.path.exists(img):
        raise ValueError(f"image slide: file not found: {img!r}")
    max_w, max_h = 9.6, 4.7
    # python-pptx keeps aspect ratio if only width given; we fit within a box.
    from PIL import Image  # Pillow ships with python-pptx
    with Image.open(img) as im:
        iw, ih = im.size
    scale = min(max_w / iw, max_h / ih, 1.0 if iw < max_w * 96 else max_w / iw)
    w = min(max_w, iw * scale)
    h = ih * (w / iw)
    if h > max_h:
        h = max_h
        w = iw * (h / ih)
    slide.shapes.add_picture(img, Inches((13.333 - w) / 2), Inches(1.55), Inches(w), Inches(h))
    if s.get("caption"):
        tf = _textbox(slide, 1.0, 6.35, 11.3, 0.5)
        _para(tf, s["caption"], theme["sizes_pt"]["caption"], color=theme["colors"]["muted"],
              font=theme["fonts"]["body"], align=PP_ALIGN.CENTER, first=True)
    _badge(slide, s.get("badge"), theme)
    _notes(slide, s.get("notes"))
    return slide


def _slide_diagram(prs, s, theme, slide_index):
    slide = _new_slide(prs)
    _h1(slide, s.get("title", ""), theme)
    nodes = {n["id"]: n for n in s.get("nodes", [])}
    kinds = {"rect": MSO_SHAPE.RECTANGLE, "rounded": MSO_SHAPE.ROUNDED_RECTANGLE,
             "ellipse": MSO_SHAPE.OVAL, "cylinder": MSO_SHAPE.CAN}
    # Connectors first (so nodes render on top of line ends)
    for e in s.get("edges", []):
        a, b = nodes.get(e["from"]), nodes.get(e["to"])
        if not a or not b:
            raise ValueError(f"diagram slide {slide_index}: edge references unknown node "
                             f"{e['from']!r}/{e['to']!r}")
        ax, ay = a["x"] + a["w"] / 2, a["y"] + a["h"] / 2
        bx, by = b["x"] + b["w"] / 2, b["y"] + b["h"] / 2
        conn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(ax), Inches(ay),
                                          Inches(bx), Inches(by))
        conn.line.color.rgb = _rgb(theme["colors"]["muted"])
        conn.line.width = Pt(1.75)
        if e.get("dashed"):
            from pptx.enum.dml import MSO_LINE_DASH_STYLE
            conn.line.dash_style = MSO_LINE_DASH_STYLE.DASH
        if e.get("label"):
            mx, my = (ax + bx) / 2, (ay + by) / 2
            tf = _textbox(slide, mx - 1.1, my - 0.16, 2.2, 0.32)
            _para(tf, e["label"], 11, color=theme["colors"]["muted"], font=theme["fonts"]["body"],
                  align=PP_ALIGN.CENTER, first=True)
    for n in s.get("nodes", []):
        kind = kinds.get(n.get("kind", "rect"), MSO_SHAPE.RECTANGLE)
        shp = _fill_rect(slide, n["x"], n["y"], n["w"], n["h"], theme["colors"]["panel"],
                         kind=kind, line_color=theme["colors"]["primary"], line_w=1.5)
        tf = shp.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        _para(tf, n.get("label", ""), theme["sizes_pt"]["body"], bold=True,
              color=theme["colors"]["ink"], font=theme["fonts"]["body"],
              align=PP_ALIGN.CENTER, first=True)
    _badge(slide, s.get("badge"), theme)
    _notes(slide, s.get("notes"))
    return slide


def build_deck(spec, theme, out_path):
    """Build the deck. Returns out_path. Raises ValueError with slide index on bad spec."""
    prs = Presentation()
    prs.slide_width = Inches(theme["canvas"]["width_in"])
    prs.slide_height = Inches(theme["canvas"]["height_in"])
    slides = spec.get("slides", [])
    total = len(slides)
    builders = {
        "title": _slide_title, "section": _slide_section, "bullets": _slide_bullets,
        "two_column": _slide_two_column, "table": _slide_table, "image": _slide_image,
    }
    project = spec.get("project", "")
    for i, s in enumerate(slides):
        stype = s.get("type")
        if stype == "diagram":
            slide = _slide_diagram(prs, s, theme, i + 1)
        elif stype in builders:
            slide = builders[stype](prs, s, theme)
        else:
            raise ValueError(f"slide {i + 1}: unknown type {stype!r}; must be one of {sorted(SLIDE_TYPES)}")
        if stype != "title":
            _footer(slide, theme, project, i, total - 1 if slides[0].get("type") == "title" else total)
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    prs.save(out_path)
    return out_path
