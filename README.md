# rm-notes

Extract annotated text from PDFs exported from reMarkable 2. Supports both yellow highlights and margin annotations (vertical lines, curly braces).

## Installation

Requires [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/clearofcant/rm-notes.git
cd rm-notes
uv sync
```

## Usage

```bash
# Output to book.md
uv run rm-notes book.pdf

# Specify output file
uv run rm-notes book.pdf -o notes.md

# Force OCR mode (for scanned/image-based PDFs)
uv run rm-notes book.pdf --ocr

# OCR with a different language (default: eng)
uv run rm-notes book.pdf --ocr --ocr-lang deu
```

## Output

```markdown
# Annotations from: book.pdf

## Page 12

> First highlighted passage from this page

> Second highlighted passage from this page

## Page 15

> Text marked with a margin brace
```

## OCR Support

For image-based PDFs (scans), the tool automatically falls back to OCR when text extraction fails. OCR requires [Tesseract](https://github.com/tesseract-ocr/tesseract) to be installed:

```bash
# Arch Linux
sudo pacman -S tesseract tesseract-data-eng

# Ubuntu/Debian
sudo apt install tesseract-ocr tesseract-ocr-eng

# macOS
brew install tesseract
```

## How it works

reMarkable exports annotations as filled shapes rather than standard PDF annotations:

- **Highlights** appear as yellow filled rectangles. The tool extracts text within these bounds.
- **Margin marks** (vertical lines, curly braces) appear as dark filled shapes. The tool extracts text spanning the vertical range of these marks.
