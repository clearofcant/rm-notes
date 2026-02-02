import argparse
import sys
from pathlib import Path

import fitz
import pytesseract
from PIL import Image


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract highlighted text from PDFs exported from reMarkable 2"
    )
    parser.add_argument("pdf_path", type=Path, help="Path to the PDF file")
    parser.add_argument(
        "-o", "--output", type=Path, help="Output Markdown file path (optional)"
    )
    parser.add_argument(
        "--ocr", action="store_true", help="Force OCR mode for text extraction"
    )
    parser.add_argument(
        "--ocr-lang", default="eng", help="Tesseract language code (default: eng)"
    )
    return parser.parse_args()


def group_rects(rects, threshold=20):
    """Group rectangles that overlap or are within threshold pixels."""
    if not rects:
        return []

    groups = []
    for rect in sorted(rects, key=lambda r: r.y0):
        for group in groups:
            for g in group:
                expanded = fitz.Rect(
                    g.x0 - threshold, g.y0 - threshold,
                    g.x1 + threshold, g.y1 + threshold
                )
                if expanded.intersects(rect):
                    group.append(rect)
                    break
            else:
                continue
            break
        else:
            groups.append([rect])
    return groups


def extract_text_ocr(page, rect, lang):
    """Extract text from a page region using OCR at 300 DPI."""
    mat = fitz.Matrix(300 / 72, 300 / 72)
    pix = page.get_pixmap(matrix=mat, clip=rect)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return pytesseract.image_to_string(img, lang=lang).strip()


def extract_highlights(pdf_path, force_ocr=False, ocr_lang="eng"):
    """Extract all highlights from a PDF, organized by page."""
    doc = fitz.open(pdf_path)
    highlights_by_page = {}

    for page_num, page in enumerate(doc, 1):
        rects = []
        for drawing in page.get_drawings():
            fill = drawing.get("fill")
            if fill and len(fill) >= 3:
                r, g, b = fill[:3]
                if r > 0.9 and g > 0.8 and b < 0.6:
                    if rect := drawing.get("rect"):
                        rects.append(fitz.Rect(rect))

        if not rects:
            continue

        page_highlights = []
        for group in group_rects(rects):
            bbox = group[0]
            for r in group[1:]:
                bbox |= r

            text = page.get_text("text", clip=bbox).strip()
            if force_ocr or len(text) < 3:
                if ocr_text := extract_text_ocr(page, bbox, ocr_lang):
                    text = ocr_text

            if text:
                page_highlights.append(text)

        if page_highlights:
            highlights_by_page[page_num] = page_highlights

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

    highlights = extract_highlights(args.pdf_path, args.ocr, args.ocr_lang)

    if not highlights:
        print("No highlights found in the PDF.", file=sys.stderr)
        sys.exit(0)

    markdown = format_markdown(highlights, args.pdf_path.name)
    output_path = args.output or args.pdf_path.with_suffix(".md")
    output_path.write_text(markdown)
    print(f"Highlights extracted to: {output_path}")


if __name__ == "__main__":
    main()
