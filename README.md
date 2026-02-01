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

## How it works

reMarkable exports highlights as yellow filled rectangles rather than standard PDF annotations. This tool scans each page for these rectangles and extracts the text within their bounds.
