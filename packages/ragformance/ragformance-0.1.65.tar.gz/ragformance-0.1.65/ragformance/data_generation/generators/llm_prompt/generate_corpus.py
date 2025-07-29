from typing import List
from ragformance.models.corpus import DocModel
import fitz
import os
from tqdm import tqdm
import json
import re


class CorpusBuilder:
    def __init__(self, pdf_folder: str, output_file: str):
        self.pdf_folder = pdf_folder
        self.output_file = output_file
        self.documents: List[DocModel] = []

    def build_corpus(self, docs_folder):
        files = [
            f
            for f in os.listdir(docs_folder)
            if f.endswith(".pdf") or f.endswith(".md")
        ]
        if not files:
            print(f"No files found in {docs_folder}")
            return
        for filename in tqdm(docs_folder, desc="Processing PDFs"):
            filepath = os.path.join(docs_folder, filename)
            name = os.path.splitext(filename)[0]
            if filepath.endswith(".pdf"):
                self.extract_text_from_pdf(filepath, name)
            if filepath.endswith(".md"):
                self.extract_text_from_md(filepath, name)

    def create_document(self, filename, page_num, text):
        document = DocModel(
            _id=f"{filename}-page={page_num+1}",
            title=f"{filename}",
            text=text,
            metadata={"document_id": filename, "page_number": page_num + 1},
        )
        self.documents.append(document)

    def extract_text_from_pdf(self, file_path: str, filename: str):
        try:
            doc = fitz.open(file_path)
        except Exception as e:
            print(f"Failed to open {file_path}: {e}")
            return
        for page_num in range(len(doc)):
            try:
                page = doc.load_page(page_num)
                text = page.get_text().strip()
                self.create_document(filename, page_num, text)
            except Exception as e:
                print(f"Failed to extract page {page_num+1} of {filename}: {e}")
        doc.close()

    def extract_text_from_md(self, file_path: str, filename: str):
        match = re.match(r".*page_(\d+).md", file_path)
        page_num = match.group(1)
        with file_path.open(encoding="utf-8") as f:
            text = f.read()
        document = self.create_document(filename, page_num, text)
        return document

    def save_to_jsonl(self):
        if not self.documents:
            print("No documents to save.")
            return

        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        with open(self.output_file, "w", encoding="utf-8") as fout:
            for doc in self.documents:
                fout.write(json.dumps(doc.to_dict(), ensure_ascii=False) + "\n")
        print(f"Saved {len(self.documents)} documents to {self.output_file}")

    def run(self):
        self.build_corpus()
        self.save_to_jsonl()


if __name__ == "__main__":
    doc_folder = ""
    output_file = "corpus.jsonl"
    builder = CorpusBuilder(doc_folder=doc_folder, output_file=output_file)
    builder.run()
