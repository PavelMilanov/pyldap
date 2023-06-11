import fitz
import re


doc = fitz.open("scan.pdf") # open a document
for page in doc:
    page.set_cropbox(fitz.Rect(0, 0, 120, 650))
    text = page.get_text()
    search = re.search(r'', text.lower())
    print(text)