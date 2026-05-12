from pathlib import Path

from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "generated"
PDF_PATH = OUT_DIR / "gui_sui_shou_poster.pdf"

FONT_NAME = "KaitiSCEmbedded"
FONT_CANDIDATES = [
    "/System/Library/Fonts/STKaiti.ttc",
    "/System/Library/Fonts/Supplemental/STKaiti.ttc",
    "/System/Library/Fonts/Supplemental/Kaiti.ttc",
    "/System/Library/AssetsV2/com_apple_MobileAsset_Font8/88d6cc32a907955efa1d014207889413890573be.asset/AssetData/Kaiti.ttc",
    "/System/Library/AssetsV2/PreinstalledAssetsV2/InstallWithOs/com_apple_MobileAsset_Font7/11a76f9d5fd800227415e64d90ddc450c8acac3e.asset/AssetData/Kaiti.ttc",
    "/System/Library/Fonts/Supplemental/Songti.ttc",
]

TITLE = "龟虽寿"
AUTHOR = "曹操"
POEM_LINES = [
    "神龟虽寿 犹有竟时",
    "腾蛇乘雾 终为土灰",
    "老骥伏枥 志在千里",
    "烈士暮年 壮心不已",
    "盈缩之期 不但在天",
    "养怡之福 可得永年",
    "幸甚至哉 歌以咏志",
]


def find_font():
    for candidate in FONT_CANDIDATES:
        path = Path(candidate)
        if path.exists():
            return str(path)
    raise FileNotFoundError("No usable Chinese font found")


def register_font():
    font_path = find_font()
    pdfmetrics.registerFont(TTFont(FONT_NAME, font_path, subfontIndex=0))
    return font_path


def draw_vertical_text(c, text, x, top_y, font_size, line_gap, color):
    c.setFillColorRGB(*color)
    c.setFont(FONT_NAME, font_size)
    y = top_y
    for char in text:
        if char.isspace():
            y -= font_size + line_gap
            continue
        c.drawCentredString(x, y - font_size, char)
        y -= font_size + line_gap


def draw_background(c, page_w, page_h):
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, page_w, page_h, stroke=0, fill=1)

    margin = 34
    c.setStrokeColorRGB(0.45, 0.45, 0.45)
    c.setLineWidth(0.65)
    c.rect(margin, margin, page_w - 2 * margin, page_h - 2 * margin, stroke=1, fill=0)

    inner = margin + 10
    c.setStrokeColorRGB(0.82, 0.82, 0.82)
    c.setLineWidth(0.25)
    c.rect(inner, inner, page_w - 2 * inner, page_h - 2 * inner, stroke=1, fill=0)


def draw_seal(c, x, y):
    size = 43
    c.setStrokeColorRGB(0.70, 0.06, 0.04)
    c.setLineWidth(1.1)
    c.roundRect(x, y, size, size, 2, stroke=1, fill=0)
    c.setFillColorRGB(0.70, 0.06, 0.04)
    c.setFont(FONT_NAME, 13)
    c.drawCentredString(x + size / 2, y + 25, "壮")
    c.drawCentredString(x + size / 2, y + 10, "心")


def make_pdf():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    register_font()

    page_size = landscape(A4)
    page_w, page_h = page_size
    pdf = canvas.Canvas(str(PDF_PATH), pagesize=page_size, pageCompression=1)
    pdf.setTitle("龟虽寿 A4 诗词海报")
    pdf.setAuthor("Codex")
    draw_background(pdf, page_w, page_h)

    title_x = page_w - 112
    draw_vertical_text(pdf, TITLE, title_x, page_h - 104, 36, 7, (0, 0, 0))
    draw_vertical_text(pdf, AUTHOR, title_x - 48, page_h - 182, 18, 5, (0.22, 0.22, 0.22))

    top_y = page_h - 98
    poem_font_size = 27
    poem_line_gap = 5
    column_gap = 74
    start_x = page_w - 235
    for index, line in enumerate(POEM_LINES):
        draw_vertical_text(
            pdf,
            line,
            start_x - index * column_gap,
            top_y,
            poem_font_size,
            poem_line_gap,
            (0, 0, 0),
        )

    draw_seal(pdf, 92, 78)
    pdf.save()
    return PDF_PATH


if __name__ == "__main__":
    print(make_pdf())
