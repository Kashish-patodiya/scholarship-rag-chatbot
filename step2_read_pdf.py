import pdfplumber

with pdfplumber.open("data/post_matric_disabilities.pdf") as pdf:
    print("Pages:", len(pdf.pages))
    for i, page in enumerate(pdf.pages[:3], start=1):
        print(f"\n--- Page {i} ---")
        text = page.extract_text()
        print(text[:500] if text else "(no text found)")


with pdfplumber.open("data/ugc_pg_scholarship.pdf") as pdf:
    print("Pages:", len(pdf.pages))
    for i, page in enumerate(pdf.pages[:3], start=1):
        print(f"\n--- Page {i} ---")
        text = page.extract_text()
        print(text[:500] if text else "(no text found)")