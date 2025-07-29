import requests
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json

import logging

logger = logging.getLogger(__name__)

# Initialize embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# In-memory storage for document embeddings
document_embeddings = []
documents = []

def upload_corpus(corpus,configpath="config.json"):

    with open(configpath, 'r') as f:
        config = json.load(f)

    document_embeddings.clear()
    documents.clear()
    documents.extend(corpus)

    # Look in the config file for the key of the dataframe where the text is stored
    text_key = config.get("corpus_text_key", "text")
    batch_size= config.get("batch_size", 32)

    # Extract texts from the corpus list
    texts = [doc[text_key] for doc in corpus]

    # Process documents in batches
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i + batch_size]

        # Generate embeddings for the batch
        batch_embeddings = embedding_model.encode(batch_texts)

        # Store embeddings
        document_embeddings.extend(batch_embeddings)

    logger.info(f"Document embeddings generated and stored in memory. {len(document_embeddings)} embeddings generated.")


def ask_queries(queries, configpath="config.json"):
    with open(configpath, 'r') as f:
        config = json.load(f)
 
    text_key = config.get("queries_text_key", "text")
    corpus_text_key = config.get("corpus_text_key", "text")
    threshold = config.get("similarity_threshold", 0.5)

    batch_size= config.get("batch_size", 32)

    url = config.get("LLM_endpoint", "https://localhost:8000/v1/chat/completions")
    key = config.get("LLM_key", None)
    model = config.get("LLM_model", None)
    if url is None or key is None or model is None:
        logger.warning("LLM endpoint, key or model not provided. Skipping LLM call.")

    # Generate embedding for the question
    # Extract texts from the corpus list
    texts = [query[text_key] for query in queries]

    query_embeddings = []

    # Process documents in batches
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i + batch_size]

        # Generate embeddings for the batch
        batch_embeddings = embedding_model.encode(batch_texts)

        # Store embeddings
        query_embeddings.extend(batch_embeddings)


    answers = []

    for qindex,query in enumerate(queries):
        question = query[text_key]
        question_embedding = query_embeddings[qindex]

        # Ensure question_embedding is a 2D array
        question_embedding = np.array([question_embedding])
        if question_embedding.ndim == 1:
            question_embedding = question_embedding.reshape(1, -1)

        # Ensure document_embeddings is a 2D array
        document_embeddings_array = np.array(document_embeddings)
        if document_embeddings_array.ndim == 1:
            document_embeddings_array = document_embeddings_array.reshape(1, -1)

        similarities = cosine_similarity(
            question_embedding,
            document_embeddings_array
        )
        relevant_documents = np.where(similarities > threshold)[1]

        logger.info(f"Query {qindex} : Found {len(relevant_documents)} relevant documents.")


        # Prepare the payload for the LLM API
        
        prompt_and_query = f"Answer the question based on the context below : \n QUESTION: {question}\n"
        for index, id in enumerate(relevant_documents):
            document = documents[id]
            text = document[corpus_text_key]
            prompt_and_query += f"CONTEXT {index + 1}: {text}\n"
        prompt_and_query += "ANSWER:"

        if url is None or key is None or model is None:

            answers.append({"query":query,"text":prompt_and_query,"relevant_documents_ids": [documents[i]["_id"] for i in relevant_documents]})
        else:
            response = requests.post(
                url=url,
                headers={
                "Authorization": "Bearer " + key,
                },
                data=json.dumps({
                "model": model,
                "messages": [
                    {
                    "role": "user",
                    "content": prompt_and_query
                    }
                ]
                })
            )

            response_json = response.json()['choices'][0]['message']['content']

            answers.append({"query":query,"text":response_json,"relevant_documents_ids": [documents[i]["_id"] for i in relevant_documents]})

    return answers
