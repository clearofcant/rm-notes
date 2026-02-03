# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

rm-notes is a Python CLI tool that extracts annotated text from PDFs exported from reMarkable 2 e-readers. Supports yellow highlights and margin annotations (vertical lines, curly braces).

## Development Commands

```bash
uv sync                           # Install dependencies
uv run rm-notes <pdf>             # Run on a PDF file
uv run rm-notes <pdf> -o out.md   # Run with custom output filename
uv run rm-notes <pdf> --ocr       # Force OCR mode for scanned PDFs
uv run rm-notes <pdf> --ocr-lang deu  # OCR with different language
```

## Architecture

Single-file design in `main.py`:
- `extract_annotations()` - Core extraction: finds yellow highlights and dark margin marks via `get_drawings()`, groups adjacent rects, extracts text (with OCR fallback)
- `group_rects()` - Groups rectangles that overlap or are within 20px threshold
- `extract_text_ocr()` - OCR fallback using pytesseract at 300 DPI
- `format_markdown()` - Converts annotations dict to Markdown output

## Key Technical Details

- reMarkable exports annotations as filled shapes, not standard PDF annotations
- Yellow highlight detection: `r > 0.9 and g > 0.8 and b < 0.6`
- Margin mark detection: dark shapes (`r,g,b < 0.5`) that are tall and narrow (`height > 15` and `height > width * 2`)
- OCR triggers automatically when text extraction returns < 3 characters
- OCR requires Tesseract installed on the system
