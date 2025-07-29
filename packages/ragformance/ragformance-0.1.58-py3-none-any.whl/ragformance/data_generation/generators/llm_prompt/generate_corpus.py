

from ragformance.models.corpus import DocModel
import fitz



# build coprus
    # for each file  (pdf or md)
        # call load text
        # create the doc onject

# load text rom pdf


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


def extract_text_from_pdf(pdf_path: str, filename: str):
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Failed to open {pdf_path}: {e}")
        return
    for page_num in range(len(doc)):
        try:
            page = doc.load_page(page_num)
            text = page.get_text().strip()
            create_document(filename, page_num, text)

        except Exception as e:
            print(f"Failed to extract page {page_num+1} of {filename}: {e}")
    doc.close()