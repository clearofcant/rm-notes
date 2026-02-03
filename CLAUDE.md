# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

rm-notes is a Python CLI tool that extracts highlighted text from PDFs exported from reMarkable 2 e-readers and converts them into Markdown files.

## Development Commands

```bash
uv sync                           # Install dependencies
uv run rm-notes <pdf>             # Run on a PDF file
uv run rm-notes <pdf> -o out.md   # Run with custom output filename
uv run rm-notes <pdf> --ocr       # Force OCR mode for scanned PDFs
```

## Architecture

Single-file design in `main.py`:
- `extract_highlights()` - Core extraction: finds yellow rectangles via `get_drawings()`, groups adjacent rects, extracts text (with OCR fallback)
- `group_rects()` - Groups highlight rectangles within 20px threshold
- `extract_text_ocr()` - OCR fallback using pytesseract at 300 DPI
- `format_markdown()` - Converts highlights dict to Markdown output

## Key Technical Details

- reMarkable exports highlights as yellow filled rectangles, not standard PDF annotations
- Yellow detection threshold: `r > 0.9 and g > 0.8 and b < 0.6`
- OCR triggers automatically when text extraction returns < 3 characters
- OCR requires Tesseract installed on the system
