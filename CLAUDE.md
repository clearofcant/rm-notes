# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

rm-notes is a Python CLI tool that extracts highlighted text from PDFs exported from reMarkable 2 e-readers and converts them into Markdown files.

## Development Commands

```bash
uv sync                           # Install dependencies
uv run rm-notes <pdf>             # Run on a PDF file
uv run rm-notes <pdf> -o out.md   # Run with custom output filename
```

## Architecture

Single-file design in `main.py` with four functions:
- `parse_args()` - CLI argument parsing
- `extract_highlights(pdf_path)` - Core extraction using PyMuPDF
- `format_markdown(highlights_by_page, pdf_name)` - Markdown output formatting
- `main()` - Entry point

## Key Technical Detail

reMarkable exports highlights as yellow filled rectangles, not standard PDF annotations. The extraction uses PyMuPDF's `get_drawings()` to find these shapes and detects yellow with threshold: `r > 0.9 and g > 0.8 and b < 0.6`.
