import logging
import os
from typing import List, Dict

from llama_index.core import VectorStoreIndex, ServiceContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.langchain import LangChainLLM
from langchain_groq import ChatGroq
from llama_index.core.schema import Document

from ragformance.models.corpus import DocModel
from ragformance.models.answer import AnnotatedQueryModel, AnswerModel
from ragformance.rag.rag_interface import RagInterface

logger = logging.getLogger(__name__)

class MultiEmbeddingLLM(RagInterface):
    def __init__(self):
        self.indexes: Dict[str, VectorStoreIndex] = {}
        self.embeddings: Dict[str, HuggingFaceEmbedding] = {}
        self.documents: List[DocModel] = []
        self.config: Dict = {}

    def upload_corpus(self, corpus: List[DocModel], config: Dict = {}) -> int:
        self.config = config or {}
        self.documents = corpus

        embedding_models_cfg = self.config.get("embedding_models", {})
        corpus_key = self.config.get("corpus_text_key", "text")

        logger.info(f"[upload_corpus] CONFIG: {self.config}")
        logger.info(f"[upload_corpus] EMBEDDINGS: {self.config.get('embedding_models', {})}")
        for emb_name, model_name in embedding_models_cfg.items():
            logger.info(f"Loading embedding model '{emb_name}': {model_name}")
            embedding = HuggingFaceEmbedding(model_name=model_name)

            docs = [Document(text=getattr(doc, corpus_key)) for doc in corpus]
            index = VectorStoreIndex.from_documents(docs, embed_model=embedding)

            self.indexes[emb_name] = index
            self.embeddings[emb_name] = embedding

        logger.info(f"{len(self.indexes)} indexes created from {len(self.documents)} documents.")
        return len(self.documents)

    def ask_queries(self, queries: List[AnnotatedQueryModel], config: Dict = {}) -> List[AnswerModel]:
        if not self.indexes:
            raise RuntimeError("You must call upload_corpus() before ask_queries().")

        config = config or self.config
        groq_key = os.getenv("groq_api_key", config["groq_api_key"])
        if not groq_key:
            raise ValueError("Missing 'groq_api_key' in config.")

        queries_key = config.get("queries_text_key", "query_text")
        llms_cfg = config.get("llms", {})
        top_k = config.get("similarity_top_k", 5)

        answers: List[AnswerModel] = []

        for query in queries:
            query_text = getattr(query, queries_key, None) or getattr(query, "query_text", None)
            if not query_text:
                logger.warning(f"Missing query text for query_id={query.query_id}, skipping.")
                continue

            for emb_name, index in self.indexes.items():
                embedding = self.embeddings[emb_name]

                for llm_name, llm_model in llms_cfg.items():
                    try:
                        llm = LangChainLLM(llm=ChatGroq(api_key=groq_key, model_name=llm_model))
                        query_engine = index.as_query_engine(
                            llm=llm,
                            embed_model=embedding,
                            similarity_top_k=top_k
                        )
                        response = query_engine.query(query_text)

                        context_docs = [
                            {"extract": node.node.get_content(), "score": node.score}
                            for node in response.source_nodes
                        ]

                        answer = AnswerModel(
                            _id=str(query.id),
                            query=query,
                            model_answer=response.response,
                            retrieved_documents_ids=[
                                node.node.node_id for node in response.source_nodes
                            ],
                        )
                        answers.append(answer)

                    except Exception as e:
                        logger.error(f"Error for {emb_name} / {llm_name} (query_id={query.query_id}): {e}")

        return answers
