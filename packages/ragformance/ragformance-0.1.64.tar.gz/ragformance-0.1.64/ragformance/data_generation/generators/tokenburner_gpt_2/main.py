import os
import re
import fitz
import io
import json
import numpy as np
from tqdm import tqdm
from collections import Counter
from openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from PIL import Image
import base64
from typing import List, Generator

# from ragformance.data_generation.generators.alpha.prompts import (
#     EXTRACT_TXT_PROMPT,
#     GENERATE_QUESTIONS_PROMPT,
#     GENERATE_ANSWERS_PROMPT,
#     FIND_CHUNKS_PROMPT,
#     CATEGORIZE_SECTIONS_PROMPT
# )
from prompts import (
    EXTRACT_TXT_PROMPT,
    GENERATE_QUESTIONS_PROMPT,
    GENERATE_ANSWERS_PROMPT,
    FIND_CHUNKS_PROMPT,
    CATEGORIZE_SECTIONS_PROMPT
)
OPENAI_API_KEY = "sk-fdf2749efde1f6e803696ff60ef06a49"
OPENAI_BASE_URL = "http://ds006asp.rd1.rf1:58401/v1"
MODEL_NAME = "gpt-4.1-mini"


#%%

def pdf_to_images(pdf_path: str) -> Generator[Image.Image, None, None]:
    doc = fitz.open(pdf_path)
    try:
        for page in doc:
            pix = page.get_pixmap()
            yield Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    finally:
        doc.close()

def image_to_bytes(image: Image.Image) -> bytes:
    with io.BytesIO() as buffer:
        image.save(buffer, format="PNG", optimize=True)
        return buffer.getvalue()


def extract_raw_text(image_b64: str, openai_client, model:str=MODEL_NAME) -> str:
    response = openai_client.chat.completions.create(
        model=model,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": EXTRACT_TXT_PROMPT}, 
                {"type": "image_url", "image_url": {
                    "url": f"data:image/png;base64,{image_b64}"
                }}
            ]
        }],
        temperature=0
    )
    return response.choices[0].message.content

def read_pdf_file_multimodal(file_path: str) -> str:
    openai_client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found")
    with fitz.open(file_path) as doc:
        total_pages = len(doc)
    print(f"Converting PDF with {total_pages} pages to images...")
    base_name = os.path.splitext(file_path)[0]
    output_txt = f"{base_name}_image_description.txt"
    with open(output_txt, "w", encoding="utf-8") as output_file:
        for page_num, image in enumerate(pdf_to_images(file_path), start=1):
            print(f"Processing page {page_num}/{total_pages}...")
            try:
                img_bytes = image_to_bytes(image)
                img_b64 = base64.b64encode(img_bytes).decode("utf-8")
                page_text = extract_raw_text(img_b64, openai_client=openai_client)
                output_file.write(f"{page_text}\n\n")
                output_file.flush()
            except Exception as e:
                error_msg = f"\nError processing page {page_num}: {str(e)}\n"
                output_file.write(error_msg)
                print(error_msg)
    print(f"Processing complete. Results saved to {output_txt}")
    return output_txt

#%%"

def remove_page_numbers(text:str)->str:
    lines = text.split('\n')
    filtered_lines = [
        line for line in lines
        if not re.fullmatch(r'^\s*p\s*a\s*g\s*e\s+\d+\s*$', line)
    ]
    return '\n'.join(filtered_lines)


#%%

def split_into_sections(raw_text:str)->List[str]:
    section_pattern = re.compile(r'\n\s*\d+\.\s+', re.IGNORECASE)
    sections = section_pattern.split(raw_text)
    chunks = []
    for i in range(1, len(sections)):
        delimiter = section_pattern.findall(raw_text)[i-1].strip()
        chunk = f"{delimiter}{sections[i]}".strip()
        chunks.append(chunk)
    return chunks

#%%

def convert_numbered_list_str_to_list(s:str)->List[str]:
    pattern = re.compile(r'^\d+\.\s*')
    values = []
    for line in s.split('\n'):
        val = pattern.sub('', line).strip()
        if val:
            values.append(val)
    return values

def generate_questions(raw_text:str, llm)->List[str]:
    prompt = GENERATE_QUESTIONS_PROMPT.format(raw_text=raw_text)
    answer = llm.invoke([HumanMessage(content=prompt)]).content.strip()
    print(answer)
    questions=convert_numbered_list_str_to_list(answer)
    return questions

def generate_answers(context:str, query:str, llm)->List[str]:
    prompt = GENERATE_ANSWERS_PROMPT.format(context=context, query=query)
    answer = llm.invoke([HumanMessage(content=prompt)])
    return answer.content.strip()


def find_chunks(context:str, query:str, llm)->List[str]:
    prompt = FIND_CHUNKS_PROMPT.format(context=context, query=query)
    chunks = llm.invoke([HumanMessage(content=prompt)])
    chunks=convert_numbered_list_str_to_list(chunks.content.strip())
    return chunks

def categorize_question(query:str, context:str, llm)->str:
    prompt = CATEGORIZE_SECTIONS_PROMPT.format(context=context, query=query)
    answer = llm.invoke([HumanMessage(content=prompt)])
    return answer.content.strip()

def extract_category(content:str):
    category_line = next(line for line in content.split('\n') if line.startswith('Category: '))
    match = re.search(r'Category:\s*\d+\.\s*(.*)', category_line)
    if match:
        category = match.group(1).strip()
        return category.lower()
    else:
        return "unknown"

#%%

def save_list_to_file(l:List[str], file_path:str)->None:
    with open(file_path, 'w') as f:
        for s in l:
            f.write(f"{s}\n")

def load_list_from_file(file_path:str)->List[str]:
    with open(file_path, 'r') as f:
        return [line.rstrip('\n') for line in f]

#%%


if __name__ == "__main__":
    # read_pdf_file_multimodal(file_path="AIDA Architecture synthesis V4.5.pdf")
    # with open("AIDA Architecture synthesis V4.5_image_description.txt", "r") as file:
    #     content = file.read()
    # content=remove_page_numbers(text=content)
    # with open("raw.txt", "w", encoding="utf-8") as f:
    #     f.write(content)

    try:
        llm = ChatOpenAI(
            model_name=MODEL_NAME,
            temperature=0.0,
            openai_api_base=OPENAI_BASE_URL,
            openai_api_key=OPENAI_API_KEY
        )
        print("LLM initialized successfully.")
    except Exception as e:
        llm = None
        print(f"Failed to initialize LLM: {e}")

    with open("raw.txt", "r") as file:
        raw_text = file.read()
    sections=split_into_sections(raw_text=raw_text)
    print("Number of sections: ", len(sections))
    questions=generate_questions(raw_text=sections[4], llm=llm)
    print(questions)

