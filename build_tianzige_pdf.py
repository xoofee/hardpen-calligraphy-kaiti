from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "generated"
CHAR_CACHE = OUT_DIR / "common_chars_level_1.txt"
PDF_PATH = OUT_DIR / "tianzige_full_workbook_vector.pdf"

FIRST_PAGE_CHARS = ["一", "二", "三", "十", "人", "大", "小", "口"]
ROWS_PER_PAGE = 16
COLS = 13
KOUZIGE_COLS = {8, 9, 10, 11, 12, 13}
NO_GRID_COLS = {1}

FONT_NAME = "KaitiSCEmbedded"
FONT_PATH = None
FONT_BBOX = None
FONT_FACE = None
GLYF_OFFSET = None
GLYPH_BBOX_CACHE = {}
FONT_CANDIDATES = [
    "/System/Library/Fonts/STKaiti.ttc",
    "/System/Library/Fonts/Supplemental/STKaiti.ttc",
    "/System/Library/Fonts/Supplemental/Kaiti.ttc",
    "/System/Library/AssetsV2/com_apple_MobileAsset_Font8/88d6cc32a907955efa1d014207889413890573be.asset/AssetData/Kaiti.ttc",
    "/System/Library/AssetsV2/PreinstalledAssetsV2/InstallWithOs/com_apple_MobileAsset_Font7/11a76f9d5fd800227415e64d90ddc450c8acac3e.asset/AssetData/Kaiti.ttc",
    "/System/Library/Fonts/Supplemental/Songti.ttc",
]


def find_font():
    for candidate in FONT_CANDIDATES:
        path = Path(candidate)
        if path.exists():
            return str(path)
    raise FileNotFoundError("No usable Chinese font found")


def register_font():
    global FONT_PATH, FONT_BBOX, FONT_FACE, GLYF_OFFSET
    font_path = find_font()
    FONT_PATH = font_path
    font = TTFont(FONT_NAME, font_path, subfontIndex=0)
    FONT_BBOX = font.face.bbox
    FONT_FACE = font.face
    GLYF_OFFSET = font.face.table["glyf"]["offset"]
    pdfmetrics.registerFont(font)
    return font_path


def glyph_bbox(char):
    if char in GLYPH_BBOX_CACHE:
        return GLYPH_BBOX_CACHE[char]
    glyph_id = FONT_FACE.charToGlyph.get(ord(char))
    if glyph_id is None:
        GLYPH_BBOX_CACHE[char] = FONT_BBOX
        return FONT_BBOX
    FONT_FACE.seek(GLYF_OFFSET + FONT_FACE.glyphPos[glyph_id])
    values = [FONT_FACE.read_short() for _ in range(5)]
    bbox = values[1:5]
    if bbox[2] <= bbox[0] or bbox[3] <= bbox[1]:
        bbox = FONT_BBOX
    GLYPH_BBOX_CACHE[char] = bbox
    return bbox


def workbook_chars():
    chars = list(CHAR_CACHE.read_text(encoding="utf-8").strip())
    ordered = []
    seen = set()
    for char in FIRST_PAGE_CHARS + chars:
        if char not in seen:
            ordered.append(char)
            seen.add(char)
    return ordered


def draw_centered_char(c, char, x, y, size, color):
    bbox = glyph_bbox(char)
    bbox_w = bbox[2] - bbox[0]
    bbox_h = bbox[3] - bbox[1]
    font_size = (size * 0.80) * 1000 / max(bbox_w, bbox_h)
    c.setFillColorRGB(*color)
    c.setFont(FONT_NAME, font_size)
    center_x = x + size / 2
    center_y = y + size / 2
    bbox_center_x = (bbox[0] + bbox[2]) / 2
    bbox_center_y = (bbox[1] + bbox[3]) / 2
    draw_x = center_x - (bbox_center_x / 1000) * font_size
    draw_y = center_y - (bbox_center_y / 1000) * font_size
    c.drawString(draw_x, draw_y, char)


def draw_cell(c, x, y, size, char=None, color=(0.1, 0.1, 0.1), grid_style="tian"):
    if grid_style != "none":
        c.setLineWidth(0.45)
        c.setStrokeColorRGB(0.25, 0.25, 0.25)
        c.rect(x, y, size, size, stroke=1, fill=0)

    if grid_style == "tian":
        c.setLineWidth(0.25)
        c.setStrokeColorRGB(0.78, 0.78, 0.78)
        c.line(x + size / 2, y, x + size / 2, y + size)
        c.line(x, y + size / 2, x + size, y + size / 2)

    if char:
        draw_centered_char(c, char, x, y, size, color)


def draw_row(c, char, x, y, size, gap):
    entries = [char] + [char] * 3 + [None] * 3 + [char] * 3 + [None] * 3
    colors = (
        [(0.02, 0.02, 0.02)]
        + [(0.74, 0.74, 0.74)] * 3
        + [(0.02, 0.02, 0.02)] * 3
        + [(0.74, 0.74, 0.74)] * 3
        + [(0.02, 0.02, 0.02)] * 3
    )
    for col, value in enumerate(entries):
        col_num = col + 1
        if col_num in NO_GRID_COLS:
            grid_style = "none"
        elif col_num in KOUZIGE_COLS:
            grid_style = "kou"
        else:
            grid_style = "tian"
        draw_cell(c, x + col * (size + gap), y, size, value, colors[col], grid_style)


def draw_page_background(c, page_w, page_h):
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, page_w, page_h, stroke=0, fill=1)


def make_pdf():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    register_font()
    chars = workbook_chars()

    page_w, page_h = A4
    col_gap = 0
    row_gap = 5.2
    cell_size = min(40.5, (page_w - margin_x * 2 - col_gap * (COLS - 1)) / COLS)
    content_w = COLS * cell_size + (COLS - 1) * col_gap
    row_pitch = cell_size + row_gap
    content_h = ROWS_PER_PAGE * cell_size + (ROWS_PER_PAGE - 1) * row_gap
    if content_w > page_w or content_h > page_h:
        raise ValueError("Grid layout does not fit on A4")
    start_x = (page_w - content_w) / 2
    start_y = (page_h + content_h) / 2 - cell_size

    pdf = canvas.Canvas(str(PDF_PATH), pagesize=A4, pageCompression=1)
    pdf.setTitle("田字格汉字描写练习")
    pdf.setAuthor("Codex")
    draw_page_background(pdf, page_w, page_h)

    for index, char in enumerate(chars):
        row_in_page = index % ROWS_PER_PAGE
        if index and row_in_page == 0:
            pdf.showPage()
            draw_page_background(pdf, page_w, page_h)
        y = start_y - row_in_page * row_pitch
        draw_row(pdf, char, start_x, y, cell_size, col_gap)

    pdf.save()
    return PDF_PATH, len(chars)


if __name__ == "__main__":
    path, count = make_pdf()
    print(path)
    print(f"characters={count}")
