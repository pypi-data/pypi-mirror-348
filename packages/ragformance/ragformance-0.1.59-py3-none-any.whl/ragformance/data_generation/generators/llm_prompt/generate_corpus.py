

from ragformance.models.corpus import DocModel
import fitz
import os
from tqdm import tqdm


# load text rom pdf
def build_corpus(docs_folder):
    documents = []
    files = [f for f in os.listdir(docs_folder) if f.endswith(".pdf") or f.endswith(".md")]
    if not files:
        print(f"No files found in {docs_folder}")
        return

    for filename in tqdm(docs_folder, desc="Processing PDFs"):
        filepath = os.path.join(docs_folder, filename)
        name = os.path.splitext(filename)[0]
        if filepath.endswith(".pdf"):
            extract_text_from_pdf(filepath, name)
        if filepath.endswith(".md"):
            extract_text_from_md(filepath, name)

# load text from md

def create_document(filename, page_num, text):
    document = DocModel(
        _id=f"{filename}-page={page_num+1}",
        title=f"{filename}",
        text=text,
        metadata={
        "document_id": filename,
        "page_number": page_num+1
            })
    return document


def extract_text_from_pdf(file_path: str, filename: str):
    documents = []
    try:
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"Failed to open {file_path}: {e}")
        return
    for page_num in range(len(doc)):
        try:
            page = doc.load_page(page_num)
            text = page.get_text().strip()
            document = create_document(filename, page_num, text)
            documents.append(document)
        except Exception as e:
            print(f"Failed to extract page {page_num+1} of {filename}: {e}")
    doc.close()

def extract_text_from_md():
    pass