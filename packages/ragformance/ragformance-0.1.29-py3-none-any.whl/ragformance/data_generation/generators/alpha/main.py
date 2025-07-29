from forcolate import convert_folders_to_markdown

from ragformance.data_generation.generators.alpha.prompts import (
    QUESTION_GENERATION_SYSTEM_PROMPT,
    QUESTION_GENERATION_USER_PROMPT,
    SUMMARIZATION_USER_PROMPT,
)
from ragformance.data_generation.generators.alpha.parsing_engine import (
    parse_qa_pairs_from_response,
    _extract_tag_content,
)
import pandas as pd
import requests
import os
import re
import json


def call_backend_agent(
    system,
    message,
    API_KEY="YOUR_KEY",
    API_URL="http://your.url/v1/chat/completions",
    API_MODEL="YOUR_MODEL",
):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
    chat_format = [
        {"role": "system", "content": system},
        {"role": "user", "content": message},
    ]
    openai_data = {
        "model": API_MODEL,
        "messages": chat_format,
        "max_tokens": -1,
        "stop": ["Observation:"],
    }
    response = requests.post(API_URL, headers=headers, json=openai_data)
    response_json = response.json()

    # Extract the assistant's message content from the response
    try:
        answer = response_json["choices"][0]["message"]["content"]

        print(answer)
        return answer
    except KeyError:
        print(f"Error: 'content' key not found in the response : {response_json}")
        return None


def summarize(
    document,
    API_KEY="YOUR_KEY",
    API_URL="http://your.url/v1/chat/completions",
    API_MODEL="YOUR_MODEL",
):
    message = SUMMARIZATION_USER_PROMPT.format(document=document)
    answer = call_backend_agent("", message, API_KEY, API_URL, API_MODEL)

    # extract the answer within <final_summary> tags
    final_summary = _extract_tag_content(answer, "final_summary")

    return final_summary


def _split_into_sentences(text: str) -> list[str]:
    """
    Splits the input text into sentences using a simple rule-based approach
    that looks for punctuation delimiters ('.', '!', '?').

    Args:
        text (str): The full document text to be split.

    Returns:
        list[str]: A list of sentence strings.
    """
    # Replace newlines with spaces for consistency
    normalized_text = text.replace("\n", " ").strip()
    if normalized_text is None or normalized_text == "":
        return []

    # Split using capturing parentheses to retain delimiters, then recombine.
    segments = re.split(r"([.!?])", normalized_text)
    sentences: list[str] = []
    for i in range(0, len(segments), 2):
        if i + 1 < len(segments):
            # Combine the text and delimiter
            candidate = (segments[i] + segments[i + 1]).strip()
        else:
            # If no delimiter segment, use the text directly
            candidate = segments[i].strip()
        if candidate:
            sentences.append(candidate)
    return sentences


def _chunk_document_fast(
    sentences: list[str],
    l_max_tokens: int,
    doc_id: str,
):
    """
    Creates chunks based purely on a maximum token length. Each sentence is added
    to the current chunk if it does not exceed l_max_tokens; otherwise, a new chunk
    is started.

    Args:
        sentences (list[str]): The list of sentences for a single document.
        l_max_tokens (int): Maximum tokens per chunk.
        doc_id (str): Unique identifier for the document.

    Returns:
        list: A list of chunk objects.
    """
    chunks: list = []
    current_chunk: list[str] = []
    current_len: int = 0
    chunk_index: int = 0

    for sentence in sentences:
        sentence_token_count = len(sentence.split())

        # If adding this sentence would exceed l_max_tokens, finalize current chunk
        if current_len + sentence_token_count > l_max_tokens:
            if current_chunk:
                chunk_str = " ".join(current_chunk)
                chunks.append((f"{doc_id}_{chunk_index}", chunk_str))
                chunk_index += 1

            # Start a new chunk with the current sentence
            current_chunk = [sentence]
            current_len = sentence_token_count
        else:
            # Add sentence to current chunk
            current_chunk.append(sentence)
            current_len += sentence_token_count

    # Any leftover chunk
    if current_chunk:
        chunk_str = " ".join(current_chunk)
        chunks.append((f"{doc_id}_{chunk_index}", chunk_str))

    return chunks


def generate_questions(
    chunks,
    file,
    summary,
    output_path="questions",
    API_KEY="YOUR_KEY",
    API_URL="http://your.url/v1/chat/completions",
    API_MODEL="YOUR_MODEL",
):
    # Assuming `chunks`, `file`, `summary`, `QUESTION_GENERATION_USER_PROMPT`,
    # `QUESTION_GENERATION_SYSTEM_PROMPT`, and `call_backend_agent` are already defined

    # List to store the data
    data = []

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for id, chunk in enumerate(chunks):
        message = QUESTION_GENERATION_USER_PROMPT.format(
            title=file.replace(".md", ""),
            document_summary=summary,
            text_chunk=chunk,
            additional_instructions="",
        )
        answer = call_backend_agent(
            QUESTION_GENERATION_SYSTEM_PROMPT, message, API_KEY, API_URL, API_MODEL
        )

        parsed_answer = parse_qa_pairs_from_response(answer)
        # check if it is a list
        if isinstance(parsed_answer, list):
            for p_answer in parsed_answer:
                # skip if no question is generated
                if (
                    p_answer is None
                    or "answer" not in p_answer
                    or len(p_answer["answer"]) == 0
                ):
                    print(f"No question generated for chunk {id} in file {file}")
                    continue
                answer = p_answer["answer"]
                if (
                    p_answer is None
                    or "question" not in p_answer
                    or len(p_answer["question"]) == 0
                ):
                    print(f"No question generated for chunk {id} in file {file}")
                    continue
                question = p_answer["question"]

                # Append the data to the list
                data.append(
                    {
                        "document_name": file.replace(".md", ""),
                        "summary": summary,
                        "chunk": chunk,
                        "question": question,
                        "answer": answer,
                    }
                )
        else:
            # If the parsed answer is not a list, handle it as a single entry
            if (
                parsed_answer is not None
                and "question" in parsed_answer
                and "answer" in parsed_answer
            ):
                question = parsed_answer["question"]
                answer = parsed_answer["answer"]

                # Append the data to the list
                data.append(
                    {
                        "document_name": file.replace(".md", ""),
                        "summary": summary,
                        "chunk": chunk,
                        "question": question,
                        "answer": answer,
                    }
                )

    if len(data) == 0:
        print(f"No questions generated for file {file}")
        return

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(data)

    # Save the DataFrame as a Parquet file
    file_path = os.path.join(output_path, f"{file.replace('.md', '')}.parquet")
    df.to_parquet(file_path, index=False)


def parquet_to_jsonl(folder_path="output"):
    # load parquet file
    corpus = []
    queries = []

    queries_id = 0

    for file in os.listdir(folder_path):
        if file.endswith(".parquet"):
            print(file)
            # read the parquet file
            df = pd.read_parquet(os.path.join(folder_path, file))

            for single_question in df.values:
                single_query = {
                    "_id": str(queries_id),
                    "text": single_question[3],
                    "references": [{"corpus_id": single_question[2][0], "score": 1}],
                    "ref_anwser": single_question[4],
                }
                queries.append(single_query)
                single_corpus = {
                    "_id": str(single_question[2][0]),
                    "title": single_question[0],
                    "text": single_question[2][1],
                }
                corpus.append(single_corpus)

                queries_id += 1

    # remove duplicates in corpus
    corpus = {v["_id"]: v for v in corpus}.values()
    corpus = list(corpus)

    pd.json_normalize(queries, max_level=0).head(10)
    corpus_path = os.path.join(folder_path, "corpus.jsonl")
    queries_path = os.path.join(folder_path, "queries.jsonl")

    # save corpus and queries to json lines files

    with open(corpus_path, "w") as f:
        for line in corpus:
            f.write(json.dumps(line) + "\n")
    with open(queries_path, "w") as f:
        for line in queries:
            f.write(json.dumps(line) + "\n")

    return corpus, queries


def run(
    folder_path: str,
    output_path: str,
    temporary_folder: str = "converted_data",
    API_KEY="YOUR_KEY",
    API_URL="http://your.url/v1/chat/completions",
    API_MODEL="YOUR_MODEL",
) -> None:
    """Convert folders to markdown files.
    Args:
        folder_path (str): Path to the folder containing the data.
        output_path (str): Path to save the converted markdown files.
    """
    # Convert the folders to markdown files
    convert_folders_to_markdown("", folder_path, temporary_folder)

    #   summarize_documents("converted_data","summarized_data") # Local version

    for file in os.listdir(temporary_folder):
        if not file.endswith(".md"):
            continue
        with open(os.path.join(temporary_folder, file)) as f:
            print(f"Reading file {file}")
            document = f.read()

            summary = summarize(document, API_KEY, API_URL, API_MODEL)

            sentences = _split_into_sentences(document)

            chunks = _chunk_document_fast(sentences, 512, file.replace(".md", ""))

            print(f"Generating questions for {file}")
            generate_questions(
                chunks, file, summary, output_path, API_KEY, API_URL, API_MODEL
            )

    # Clean up the temporary folder
    return parquet_to_jsonl(output_path)
