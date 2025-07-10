import os
import pymupdf
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
        try:
            doc = pymupdf.open(filepath)
            text = ""
            for page in doc:
                text += page.get_text("text")
            doc.close()
            return text
        except Exception as e:
            raise ValueError(f"Error reading PDF file: {str(e)}")

    else:
        raise ValueError("Only .md or .pdf files are supported")
