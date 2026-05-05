# 硬笔楷体田字格练习册

这是一个用于生成硬笔楷体汉字练习纸的项目。当前已生成两份 PDF，可直接打开、打印或分发使用。

## 已生成 PDF

- [田字格汉字描写练习册](generated/tianzige_full_workbook_vector.pdf)
- [空白田字格 / 口字格练习纸](generated/blank_tianzige_kouzige_exercise.pdf)

## 内容说明

### 田字格汉字描写练习册

文件：`generated/tianzige_full_workbook_vector.pdf`

这份 PDF 使用常用规范汉字生成练习页。每一行包含示范字、浅色描红字、田字格练习格，以及口字格练习格，适合按字逐行练习硬笔楷体结构。

### 空白田字格 / 口字格练习纸

文件：`generated/blank_tianzige_kouzige_exercise.pdf`

这份 PDF 是空白练习纸，左侧为田字格，右侧为口字格，适合自由临写、默写或课堂练习。

## 重新生成

项目中的脚本会把输出文件写入 `generated/` 目录。

```bash
python3 build_tianzige_pdf.py
python3 build_blank_grid_pdf.py
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
