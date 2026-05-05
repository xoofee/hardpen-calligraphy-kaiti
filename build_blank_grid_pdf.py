from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "generated"
PDF_PATH = OUT_DIR / "blank_tianzige_kouzige_exercise.pdf"

ROWS = 16
COLS = 12
TIAN_COLS = set(range(1, 7))


def draw_page_background(c, page_w, page_h):
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, page_w, page_h, stroke=0, fill=1)


def draw_cell(c, x, y, size, grid_style):
    c.setLineWidth(0.45)
    c.setStrokeColorRGB(0.25, 0.25, 0.25)
    c.rect(x, y, size, size, stroke=1, fill=0)

    if grid_style == "tian":
        c.setLineWidth(0.25)
        c.setStrokeColorRGB(0.78, 0.78, 0.78)
        c.line(x + size / 2, y, x + size / 2, y + size)
        c.line(x, y + size / 2, x + size, y + size / 2)


def make_pdf():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    page_w, page_h = A4
    col_gap = 0
    row_gap = 5.2
    cell_size = 40.5
    content_w = COLS * cell_size + (COLS - 1) * col_gap
    content_h = ROWS * cell_size + (ROWS - 1) * row_gap
    if content_w > page_w or content_h > page_h:
        raise ValueError("Grid layout does not fit on A4")

    start_x = (page_w - content_w) / 2
    start_y = (page_h + content_h) / 2 - cell_size

    pdf = canvas.Canvas(str(PDF_PATH), pagesize=A4, pageCompression=1)
    pdf.setTitle("空白田字格口字格练习纸")
    pdf.setAuthor("Codex")
    draw_page_background(pdf, page_w, page_h)

    for row in range(ROWS):
        y = start_y - row * (cell_size + row_gap)
        for col in range(COLS):
            x = start_x + col * (cell_size + col_gap)
            grid_style = "tian" if (col + 1) in TIAN_COLS else "kou"
            draw_cell(pdf, x, y, cell_size, grid_style)

    pdf.save()
    return PDF_PATH


if __name__ == "__main__":
    print(make_pdf())
