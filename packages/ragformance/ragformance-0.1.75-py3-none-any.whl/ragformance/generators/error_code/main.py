from ragformance.generators.generators.error_code.parsing_engine import (
    find_pages,
    merge_pages,
    extract_keywords,
)
from ragformance.generators.generators.error_code.question_generation import (
    generate_easy_question,
    question_variation,
    add_augmented_question,
)
import numpy as np


def run(
    folder_path: str,
    prefix_id: str,
    title: str,
    max_token_context=64000,
    tag=[],
    category="error code",
    keywords="error, information, or alarm codes (e.g., E09)",
    API_KEY=None,
    API_URL="http://your.url/v1/chat/completions",
    API_MODEL=None,
):
    # todo : iterate over all files in the folder
    # extract title and prefix from the file or an additional file
    with open(folder_path + "/output.md", encoding="utf-8") as file:
        manual = file.read()

    page_numbers = find_pages(
        keywords,
        manual,
        max_token_context=max_token_context,
        API_KEY=API_KEY,
        API_URL=API_URL,
        API_MODEL=API_MODEL,
    )

    if len(page_numbers) == 0:
        return

    tempory_file, _ = merge_pages(page_numbers, folder_path, prefix_id, title)
    err_code = extract_keywords(
        keywords, tempory_file, API_KEY=API_KEY, API_URL=API_URL, API_MODEL=API_MODEL
    )

    # Specialized on Error Code
    queries, query_augmentation = generate_easy_question(
        err_code, category=category, tags=tag, prefix_id=prefix_id
    )

    # TO DO
    # med_keywords = "clean the device, diagnosis, troubleshooting, and other related information for repairing the device"
    # med_page_numbers = find_pages(med_keywords, manual, max_token_context=max_token_context, API_KEY=API_KEY, API_URL=API_URL, API_MODEL=API_MODEL)
    # tempory_file, _ = merge_pages(med_page_numbers, folder_path, prefix_id, title)
    # med_queries, med_query_augmentation = generate_med_question(err_code, tempory_file, category=category, tags=tag, prefix_id=prefix_id, API_KEY=API_KEY, API_URL=API_URL, API_MODEL=API_MODEL)

    # queries.extend(med_queries)
    # query_augmentation.extend(med_query_augmentation)
    # page_numbers.extend(med_page_numbers)

    augmented_question = question_variation(
        query_augmentation, API_KEY=API_KEY, API_URL=API_URL, API_MODEL=API_MODEL
    )
    queries = add_augmented_question(queries, augmented_question)
    tempory_file, corpus = merge_pages(
        np.unique(page_numbers), folder_path, prefix_id, title
    )

    return corpus, queries
