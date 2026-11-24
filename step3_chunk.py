import fitz  # PyMuPDF
import re
import json
import glob
import os

MAX_WORDS = 300   # ek chunk mein zyada se zyada itne shabd
OVERLAP = 50      # lambe section todte waqt itne shabd repeat honge

# Heading jaisi line: "1. OBJECTIVE", "4. ELIGIBILITY OF INSTITUTIONS"
HEADING = re.compile(r"^\s*\d{1,2}(\.\d{1,2})*[\.\)]?\s+[A-Z][A-Z ,&/\-\(\)]{3,}$")


def read_pdf(path):
    """PDF se (page_number, text) ki list nikalo."""
    doc = fitz.open(path)
    pages = []
    for i, page in enumerate(doc, start=1):
        try:
            pages.append((i, page.get_text()))
        except Exception as e:
            print(f"  Warning: page {i} nahi padha ja saka ({e})")
            pages.append((i, ""))
    return pages


def split_into_sections(pages):
    """Headings ke hisaab se sections banao. Har section ka page number yaad rakho."""
    sections = []
    current = {"heading": "Introduction", "page": 1, "lines": []}

    for page_num, text in pages:
        for line in text.split("\n"):
            if HEADING.match(line):
                # purana section band karo, naya shuru karo
                if current["lines"]:
                    sections.append(current)
                current = {"heading": line.strip(), "page": page_num, "lines": []}
            else:
                if line.strip():
                    current["lines"].append(line.strip())
    if current["lines"]:
        sections.append(current)
    return sections


def split_long_text(text):
    """Lambe text ko overlap ke saath todo."""
    words = text.split()
    if len(words) <= MAX_WORDS:
        return [text]
    parts = []
    step = MAX_WORDS - OVERLAP
    for start in range(0, len(words), step):
        parts.append(" ".join(words[start:start + MAX_WORDS]))
        if start + MAX_WORDS >= len(words):
            break
    return parts


def make_chunks(path):
    filename = os.path.basename(path)
    # file ke naam se scheme ka naam banao (abhi simple tareeka)
    scheme = os.path.splitext(filename)[0].replace("_", " ")

    pages = read_pdf(path)
    empty_pages = sum(1 for _, t in pages if not t.strip())
    if empty_pages:
        print(f"  Warning: {empty_pages} page(s) mein text nahi mila (scanned ya kharab?)")

    chunks = []
    for sec in split_into_sections(pages):
        body = " ".join(sec["lines"])
        for part in split_long_text(body):
            if len(part.split()) < 10:
                continue  # bahut chhote tukde chhod do
            chunks.append({
                "source": filename,
                "scheme": scheme,
                "heading": sec["heading"],
                "page": sec["page"],
                # embedding ke liye: scheme + heading + text
                "text": f"Scheme: {scheme} | Section: {sec['heading']}\n{part}",
            })
    return chunks


all_chunks = []
for pdf_path in sorted(glob.glob("data/*.pdf")):
    print(f"Processing: {pdf_path}")
    chunks = make_chunks(pdf_path)
    print(f"  -> {len(chunks)} chunks")
    all_chunks.extend(chunks)

with open("chunks.json", "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, ensure_ascii=False, indent=2)

print(f"\nTotal chunks: {len(all_chunks)}")
if all_chunks:
    print("\n--- Sample chunk ---")
    print(json.dumps(all_chunks[min(3, len(all_chunks) - 1)], indent=2, ensure_ascii=False))