# rm-notes

Extract highlighted text from PDFs exported from reMarkable 2.

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
# Highlights from: book.pdf

## Page 12

> First highlighted phrase from this page

> Second highlighted phrase from this page

## Page 15

> Another highlight here
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

reMarkable exports highlights as yellow filled rectangles rather than standard PDF annotations. This tool scans each page for these rectangles and extracts the text within their bounds.
