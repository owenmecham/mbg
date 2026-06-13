#!/usr/bin/env python3
"""
generate_brand_board.py
MBG Brand Intelligence Plugin — Brand Board PDF Generator

Usage:
    python3 generate_brand_board.py /path/to/brand-{slug}.json

Output:
    /mnt/outputs/brand-{slug}-brand-board.pdf

Dependencies:
    pip install reportlab Pillow fonttools --break-system-packages -q
"""

import json
import sys
import os
import math
from pathlib import Path

# ── Output path ──────────────────────────────────────────────────────────────
OUTPUT_DIR = "/mnt/outputs"

# ── ReportLab imports ─────────────────────────────────────────────────────────
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.pdfgen import canvas as rl_canvas
    from reportlab.lib.colors import HexColor, white, black
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
except ImportError:
    print("Installing reportlab...")
    os.system("pip install reportlab --break-system-packages -q")
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.pdfgen import canvas as rl_canvas
    from reportlab.lib.colors import HexColor, white, black
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    os.system("pip install Pillow --break-system-packages -q")
    from PIL import Image, ImageDraw, ImageFont


# ── Helpers ───────────────────────────────────────────────────────────────────

def hex_to_color(hex_str, fallback="#333333"):
    """Convert hex string to ReportLab HexColor, with fallback."""
    if not hex_str or not str(hex_str).strip():
        hex_str = fallback
    h = str(hex_str).strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        h = fallback.lstrip("#")
    try:
        return HexColor(f"#{h}")
    except Exception:
        return HexColor(fallback)


def lighten_hex(hex_str, factor=0.92):
    """Return a lightened version of a hex color for backgrounds."""
    h = hex_str.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    return f"#{r:02x}{g:02x}{b:02x}"


def register_font(name, path, fallback="Helvetica"):
    """Register a TTF font with ReportLab. Returns registered name or fallback."""
    if not path or not os.path.exists(path):
        return fallback
    try:
        pdfmetrics.registerFont(TTFont(name, path))
        return name
    except Exception as e:
        print(f"  [warn] Could not register font '{name}' from {path}: {e}")
        return fallback


def draw_shadow_rect(c, x, y, w, h, shadow_offset=3, shadow_alpha=0.18):
    """Draw a soft drop shadow beneath a rectangle."""
    shadow_color = HexColor("#000000")
    c.saveState()
    c.setFillColor(shadow_color)
    c.setFillAlpha(shadow_alpha)
    c.rect(x + shadow_offset, y - shadow_offset, w, h, fill=1, stroke=0)
    c.restoreState()


def wrap_text(text, max_chars):
    """Simple word-wrap returning a list of lines."""
    words = str(text).split()
    lines, current = [], ""
    for word in words:
        if len(current) + len(word) + 1 <= max_chars:
            current = f"{current} {word}".strip()
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


# ── Main generator ────────────────────────────────────────────────────────────

def generate_brand_board(brand_json_path: str):
    with open(brand_json_path, "r") as f:
        brand = json.load(f)

    slug = brand.get("slug", "brand")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, f"brand-{slug}-brand-board.pdf")

    # ── Pull brand data ───────────────────────────────────────────────────────
    identity = brand.get("identity", {})
    contact = brand.get("contact", {})
    social = brand.get("social", {})
    colors = brand.get("colors", {})
    typography = brand.get("typography", {})
    font_files = typography.get("font_files", {})
    assets = brand.get("assets", {})
    voice = brand.get("voice", {})

    brand_name = brand.get("brand_name", identity.get("company_name", "Your Brand"))
    full_name = identity.get("full_name", "")
    title = identity.get("title", "")
    tagline = identity.get("tagline", "")
    city_state = identity.get("city_state", "")

    primary_hex = colors.get("primary", "#2C4A6E")
    secondary_hex = colors.get("secondary", "#4A8B7F")
    accent_hex = colors.get("accent", "#E8A838")
    text_hex = colors.get("text", "#1A1A1A")
    bg_hex = colors.get("background", "#FFFFFF")
    extended_palette = colors.get("extended_palette", [])

    heading_font_name = typography.get("heading_font", "Montserrat")
    body_font_name = typography.get("body_font", "Open Sans")
    script_font_name = typography.get("script_font", "")

    # ── Register fonts ────────────────────────────────────────────────────────
    h_font = register_font("BrandHeading", font_files.get("heading"), "Helvetica-Bold")
    b_font = register_font("BrandBody", font_files.get("body"), "Helvetica")
    s_font = register_font("BrandScript", font_files.get("script"), h_font)

    # ── Page setup ────────────────────────────────────────────────────────────
    PAGE_W, PAGE_H = 11 * inch, 8.5 * inch  # landscape letter
    c = rl_canvas.Canvas(output_path, pagesize=(PAGE_W, PAGE_H))

    # Background — very light tint of primary color
    bg_light = lighten_hex(primary_hex, 0.96)
    c.setFillColor(hex_to_color(bg_light))
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    MARGIN = 0.45 * inch
    LEFT_COL_W = 3.2 * inch
    RIGHT_COL_X = MARGIN + LEFT_COL_W + 0.35 * inch
    RIGHT_COL_W = PAGE_W - RIGHT_COL_X - MARGIN

    # ── Left column — Polaroid color swatches ─────────────────────────────────
    swatch_colors = [
        (primary_hex, "Primary"),
        (secondary_hex, "Secondary"),
        (accent_hex, "Accent"),
        (text_hex, "Text"),
        (bg_hex, "Background"),
    ]
    # Add extras from extended palette
    for i, ec in enumerate(extended_palette[:2]):
        swatch_colors.append((ec, f"Extended {i+1}"))

    SWATCH_W = 1.35 * inch
    SWATCH_H = 1.0 * inch
    FOOTER_H = 0.38 * inch
    GAP = 0.18 * inch

    # 3-2 staggered grid
    row1 = swatch_colors[:3]
    row2 = swatch_colors[3:5]

    def draw_polaroid(cx, cy, hex_color, label):
        sw, sh, fh = SWATCH_W, SWATCH_H, FOOTER_H
        x = cx - sw / 2
        y = cy
        full_h = sh + fh
        draw_shadow_rect(c, x, y, sw, full_h, shadow_offset=4, shadow_alpha=0.15)
        # White frame
        c.setFillColor(white)
        c.rect(x, y, sw, full_h, fill=1, stroke=0)
        # Color block
        c.setFillColor(hex_to_color(hex_color))
        c.rect(x, y + fh, sw, sh, fill=1, stroke=0)
        # Label in footer
        c.setFillColor(hex_to_color(text_hex))
        c.setFont(b_font, 6.5)
        c.drawCentredString(cx, y + fh * 0.62, label)
        c.setFont(b_font, 5.5)
        c.drawCentredString(cx, y + fh * 0.25, hex_color.upper())

    top_y = PAGE_H - MARGIN - SWATCH_H - FOOTER_H
    # Row 1 (3 swatches)
    for i, (hx, lbl) in enumerate(row1):
        cx = MARGIN + SWATCH_W / 2 + i * (SWATCH_W + GAP)
        draw_polaroid(cx, top_y, hx, lbl)

    # Row 2 (2 swatches, centered)
    row2_start_x = MARGIN + (SWATCH_W + GAP) / 2
    row2_y = top_y - SWATCH_H - FOOTER_H - GAP * 1.8
    for i, (hx, lbl) in enumerate(row2):
        cx = row2_start_x + SWATCH_W / 2 + i * (SWATCH_W + GAP)
        draw_polaroid(cx, row2_y, hx, lbl)

    # ── Right column — Brand identity ─────────────────────────────────────────
    rx = RIGHT_COL_X
    ry = PAGE_H - MARGIN

    # Brand name in script font (large)
    script_size = 38
    c.setFillColor(hex_to_color(primary_hex))
    c.setFont(s_font, script_size)
    ry -= script_size * 1.15
    c.drawString(rx, ry, brand_name)

    # Full name + title in heading font
    ry -= 0.22 * inch
    c.setFont(h_font, 14)
    c.setFillColor(hex_to_color(text_hex))
    namestr = full_name
    if title:
        namestr = f"{full_name}  |  {title}" if full_name else title
    c.drawString(rx, ry, namestr)

    # Tagline in italic body font
    if tagline:
        ry -= 0.22 * inch
        c.setFont(b_font, 10)
        c.setFillColor(hex_to_color(secondary_hex))
        c.drawString(rx, ry, f'"{tagline}"')

    # ── Horizontal color bar ──────────────────────────────────────────────────
    ry -= 0.3 * inch
    bar_h = 0.18 * inch
    bar_colors = [primary_hex, secondary_hex, accent_hex] + extended_palette[:2]
    seg_w = RIGHT_COL_W / len(bar_colors)
    for i, bh in enumerate(bar_colors):
        c.setFillColor(hex_to_color(bh))
        c.rect(rx + i * seg_w, ry - bar_h, seg_w, bar_h, fill=1, stroke=0)
    ry -= bar_h + 0.25 * inch

    # ── Typography panels ─────────────────────────────────────────────────────
    panel_h = 0.72 * inch
    panel_gap = 0.15 * inch
    panel_w = (RIGHT_COL_W - panel_gap) / 2
    panel_bg = hex_to_color(lighten_hex(primary_hex, 0.94))

    def draw_font_panel(px, py, font_name, font_reg, label):
        c.setFillColor(panel_bg)
        c.rect(px, py, panel_w, panel_h, fill=1, stroke=0)
        c.setFillColor(hex_to_color(text_hex))
        c.setFont(b_font, 7)
        c.drawString(px + 8, py + panel_h - 14, label.upper())
        c.setFont(font_reg, 16)
        c.drawString(px + 8, py + panel_h * 0.38, font_name[:22])
        c.setFont(b_font, 7)
        c.setFillColor(hex_to_color(secondary_hex))
        c.drawString(px + 8, py + 7, "Aa Bb Cc 123")

    draw_font_panel(rx, ry - panel_h, heading_font_name, h_font, "Heading Font")
    draw_font_panel(rx + panel_w + panel_gap, ry - panel_h, body_font_name, b_font, "Body Font")
    ry -= panel_h + 0.28 * inch

    # ── Brand voice adjective pills ───────────────────────────────────────────
    adjectives = voice.get("personality_adjectives", [])
    if adjectives:
        pill_colors = [primary_hex, secondary_hex, accent_hex, primary_hex, secondary_hex]
        px = rx
        for idx, adj in enumerate(adjectives[:6]):
            pill_color = hex_to_color(pill_colors[idx % len(pill_colors)])
            pill_w = max(len(adj) * 6.5 + 16, 60)
            pill_h = 18
            c.setFillColor(pill_color)
            c.roundRect(px, ry - pill_h, pill_w, pill_h, 4, fill=1, stroke=0)
            c.setFillColor(white)
            c.setFont(b_font, 8)
            c.drawCentredString(px + pill_w / 2, ry - pill_h + 5, adj.title())
            px += pill_w + 8
            if px > rx + RIGHT_COL_W - 60:
                break
        ry -= pill_h + 0.2 * inch

    # ── Contact info ──────────────────────────────────────────────────────────
    contact_items = []
    if contact.get("website"):
        contact_items.append(f"🌐  {contact['website']}")
    if contact.get("email"):
        contact_items.append(f"✉  {contact['email']}")
    if contact.get("phone"):
        contact_items.append(f"📞  {contact['phone']}")
    if city_state:
        contact_items.append(f"📍  {city_state}")

    for item in contact_items:
        ry -= 0.18 * inch
        c.setFillColor(hex_to_color(text_hex))
        c.setFont(b_font, 8.5)
        c.drawString(rx, ry, item)

    # ── Social handles ────────────────────────────────────────────────────────
    social_items = []
    platform_labels = [
        ("instagram", "IG"), ("tiktok", "TK"), ("youtube", "YT"),
        ("linkedin", "LI"), ("facebook", "FB"), ("threads", "TH"),
    ]
    for key, abbr in platform_labels:
        val = social.get(key, "")
        if val:
            handle = val.lstrip("@").lstrip("https://").split("/")[-1]
            social_items.append((abbr, f"@{handle}" if not handle.startswith("@") else handle))

    if social_items:
        ry -= 0.22 * inch
        sx = rx
        for abbr, handle in social_items[:6]:
            circle_r = 10
            c.setFillColor(hex_to_color(accent_hex))
            c.circle(sx + circle_r, ry, circle_r, fill=1, stroke=0)
            c.setFillColor(white)
            c.setFont(h_font, 6)
            c.drawCentredString(sx + circle_r, ry - 2.5, abbr)
            c.setFillColor(hex_to_color(text_hex))
            c.setFont(b_font, 7.5)
            c.drawString(sx + circle_r * 2 + 5, ry - 3, handle)
            sx += circle_r * 2 + len(handle) * 4.8 + 16

    # ── Bottom full-width color bar with names ────────────────────────────────
    bar_y = MARGIN * 0.6
    full_bar_h = 0.22 * inch
    seg_w2 = PAGE_W / len(bar_colors)
    for i, bh in enumerate(bar_colors):
        c.setFillColor(hex_to_color(bh))
        c.rect(i * seg_w2, bar_y, seg_w2, full_bar_h, fill=1, stroke=0)
        # Color name label centered in segment
        swatch_name = [lbl for hx, lbl in swatch_colors if hx == bh]
        lbl_text = swatch_name[0] if swatch_name else ""
        c.setFillColor(white)
        c.setFont(b_font, 6)
        c.drawCentredString(i * seg_w2 + seg_w2 / 2, bar_y + full_bar_h * 0.28, lbl_text.upper())

    # Footer label
    c.setFillColor(hex_to_color(text_hex))
    c.setFont(b_font, 6.5)
    c.setFillAlpha(0.45)
    c.drawCentredString(PAGE_W / 2, bar_y - 10, f"BRAND KIT  ·  {brand_name.upper()}  ·  PREPARED BY MYBUSINESSGENIE")
    c.setFillAlpha(1.0)

    # ── Left column bottom — target audience / brand voice note ───────────────
    audience = voice.get("target_audience", "")
    tone = voice.get("tone", "")
    if audience or tone:
        note_y = row2_y - 0.35 * inch
        c.setFillColor(hex_to_color(text_hex))
        c.setFont(h_font, 7)
        c.drawString(MARGIN, note_y, "AUDIENCE")
        note_y -= 0.16 * inch
        c.setFont(b_font, 7.5)
        if audience:
            for line in wrap_text(audience, 34)[:3]:
                c.drawString(MARGIN, note_y, line)
                note_y -= 0.14 * inch
        if tone:
            note_y -= 0.08 * inch
            c.setFont(h_font, 7)
            c.drawString(MARGIN, note_y, "TONE")
            note_y -= 0.16 * inch
            c.setFont(b_font, 7.5)
            c.drawString(MARGIN, note_y, tone[:50])

    c.save()
    print(f"✅ Brand board saved: {output_path}")
    return output_path


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 generate_brand_board.py /path/to/brand-{slug}.json")
        sys.exit(1)

    brand_path = sys.argv[1]
    if not os.path.exists(brand_path):
        print(f"Error: File not found: {brand_path}")
        sys.exit(1)

    try:
        result = generate_brand_board(brand_path)
        print(f"Brand board generated at: {result}")
    except Exception as e:
        print(f"Error generating brand board: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
