# 硬笔楷体田字格练习册

这是一个用于生成硬笔楷体汉字练习纸的项目。当前已生成两份 PDF，可直接打开、打印或分发使用。

## 已生成 PDF

- [田字格汉字描写练习册](generated/tianzige_full_workbook_vector.pdf)
- [横画专项田字格描写练习册](generated/horizontal_stroke_training.pdf)
- [空白田字格 / 口字格练习纸](generated/blank_tianzige_kouzige_exercise.pdf)


## 内容说明

### 田字格汉字描写练习册

文件：`generated/tianzige_full_workbook_vector.pdf`

这份 PDF 使用常用规范汉字生成练习页。每一行包含示范字、浅色描红字、田字格练习格，以及口字格练习格，适合按字逐行练习硬笔楷体结构。

练习册的汉字顺序来自 `generated/common_chars_level_1.txt`。这个文件由 `build_tianzige_workbook.py` 首次运行时从“通用规范汉字一级字表”页面抓取并缓存，后续生成会直接复用该缓存，以保持练习顺序稳定。

脚本会把 `一`、`二`、`三`、`十`、`人`、`大`、`小`、`口` 放在最前面，方便从基础笔画和简单结构开始练习；后面的汉字按 `common_chars_level_1.txt` 中的顺序排列。

### 横画专项田字格描写练习册

文件：`generated/horizontal_stroke_training.pdf`

这份 PDF 用于专项练习横画，从 `一`、`二`、`三` 开始，逐步过渡到 `目`、`量` 等横画较多的汉字。页面结构与主练习册一致，包含示范字、浅色描红字、田字格练习格和口字格练习格。

### 空白田字格 / 口字格练习纸

文件：`generated/blank_tianzige_kouzige_exercise.pdf`

这份 PDF 是空白练习纸，左侧为田字格，右侧为口字格，适合自由临写、默写或课堂练习。

### 《龟虽寿》A4 诗词海报

文件：`generated/gui_sui_shou_poster.pdf`

这份 PDF 是横版 A4 诗词海报，使用楷体竖排《龟虽寿》全文，并省去标点，适合打印后张贴。

## 重新生成

项目中的脚本会把输出文件写入 `generated/` 目录。

```bash
python3 build_tianzige_pdf.py
python3 build_horizontal_stroke_pdf.py
python3 build_blank_grid_pdf.py
python3 build_gui_sui_shou_poster.py
```

如果需要生成 Word 版本练习册，可以运行：

```bash
python3 build_tianzige_workbook.py
```

## 依赖

主要依赖：

- `reportlab`
- `python-docx`
- `Pillow`

生成练习册时会优先使用系统中的楷体字体；如果没有可用楷体字体，脚本会尝试使用其他中文字体。
