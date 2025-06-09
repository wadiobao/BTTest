
import os
import pdfplumber
import markdown2
from bs4 import BeautifulSoup


def extract_text_from_file(filepath: str) -> str:
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".md":
        with open(filepath, "r", encoding="utf-8") as f:
            markdown_content = f.read()
            html = markdown2.markdown(markdown_content)
            soup = BeautifulSoup(html, "html.parser")
            return soup.get_text()

    elif ext == ".pdf":
        with pdfplumber.open(filepath) as pdf:
            pages = [page.extract_text() for page in pdf.pages if page.extract_text()]
            return "\n".join(pages)

    else:
        raise ValueError("Chỉ hỗ trợ file .md hoặc .pdf")
