import argparse
import sys
from pathlib import Path

import fitz


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract highlighted text from PDFs exported from reMarkable 2"
    )
    parser.add_argument("pdf_path", type=Path, help="Path to the PDF file")
    parser.add_argument(
        "-o", "--output", type=Path, help="Output Markdown file path (optional)"
    )
    return parser.parse_args()


def extract_highlights(pdf_path):
    """Extract all highlights from a PDF, organized by page."""
    doc = fitz.open(pdf_path)
    highlights_by_page = {}

    for page_num in range(len(doc)):
        page = doc[page_num]
        page_highlights = []

        # reMarkable exports highlights as yellow filled rectangles
        for drawing in page.get_drawings():
            fill = drawing.get("fill")
            if fill and len(fill) >= 3:
                r, g, b = fill[0], fill[1], fill[2]
                if r > 0.9 and g > 0.8 and b < 0.6:  # Yellow highlight
                    rect = drawing.get("rect")
                    if rect:
                        text = page.get_text("text", clip=rect).strip()
                        if text:
                            page_highlights.append(text)

        if page_highlights:
            highlights_by_page[page_num + 1] = page_highlights

    doc.close()
    return highlights_by_page


def format_markdown(highlights_by_page, pdf_name):
    """Convert highlights to Markdown format."""
    lines = [f"# Highlights from: {pdf_name}", ""]

    for page_num in sorted(highlights_by_page.keys()):
        lines.append(f"## Page {page_num}")
        lines.append("")
        for highlight in highlights_by_page[page_num]:
            lines.append(f"> {highlight}")
            lines.append("")

    return "\n".join(lines)


def main():
    args = parse_args()

    if not args.pdf_path.exists():
        print(f"Error: File not found: {args.pdf_path}", file=sys.stderr)
        sys.exit(1)

    highlights = extract_highlights(args.pdf_path)

    if not highlights:
        print("No highlights found in the PDF.", file=sys.stderr)
        sys.exit(0)

    markdown = format_markdown(highlights, args.pdf_path.name)
    output_path = args.output or args.pdf_path.with_suffix(".md")
    output_path.write_text(markdown)
    print(f"Highlights extracted to: {output_path}")


if __name__ == "__main__":
    main()
