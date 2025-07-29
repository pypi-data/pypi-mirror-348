import logging
import pandas as pd
from pathlib import Path
import json
from tqdm import tqdm
from typing import List, Optional
import uuid

from ragformance.rag.rag_interface import RagInterface
from ragformance.models.corpus import DocModel
from ragformance.models.answer import AnnotatedQueryModel, AnswerModel

from ragformance.rag.clients.ollama_client import OllamaClient
from ragformance.rag.clients.openwebui_client import OpenWebUIClient


logging.basicConfig(level=logging.INFO)


# Run the following docker command 
# docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
# docker run -d -p 3000:8080 --gpus all --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:cuda

class OpenwebuiRag(RagInterface):
    
    def upload_corpus(self, corpus: List[DocModel], config_p: Optional[Path] = None):
    
        
        client = OpenWebUIClient("http://localhost:3000")

        id_column = DocModel.id
        content_column = DocModel.text

        config = {}
        if config_p and config_p.exists():
            with open(config_p, "r") as f:
                config = json.load(f)
    
        model_name = config.get("model_name", "not_referenced")
        dataset_name = config.get("dataset_name", "not_referenced")
        client_email = config.get("client_email", "admin@example.com")
        client_mdp = config.get("client_mdp", "admin")
        
        client.sign_in(client_email,client_mdp)

        
        collection_name = f"Benchmark_{dataset_name.replace(' ', '_')}_{model_name.replace(':', '_').replace('/', '_')}"
        coll_info = None
    
        try:
            logging.info(
                f"Début du benchmark pour le dataset '{dataset_name}' avec le modèle '{model_name}'."
            )
            coll_info = client.create_collection(
                name=collection_name,
                description=f"Collection de benchmark pour {dataset_name} avec {model_name}",
            )
    
            if not coll_info or "id" not in coll_info:
                logging.error(
                    f"Échec de la création ou de la récupération de la collection '{collection_name}'."
                )
                return pd.DataFrame([])  # Retourne un DF vide
    
            collection_id = coll_info["id"]
            logging.info(f"Utilisation de la collection ID: {collection_id}")
    
            add_results = client.add_documents_from_df_to_collection(
                df=corpus,
                collection_id=collection_id,
                doc_id_column=id_column,
                content_column=content_column,
            )
            
            logging.info(f"Résultats de l'ajout des documents du CSV: {add_results}")
    
            config["Collection_ID"] = collection_id
            
            with open(config_p, 'w') as f:
                json.dump(config, f)

        
       
        except Exception as e:
            logging.error(
                f"Une erreur est survenue durant l'upload du corpus: {e}", exc_info=True
            )

        return add_results["processed_count"]
    
    
    
    
    def ask_queries(
        self, queries: List[AnnotatedQueryModel], config_p: Optional[Path] = None
    ):
    
        
        client = OpenWebUIClient("http://localhost:3000")
        ollama_client = OllamaClient("http://localhost:11434")
        
        
        config = {}
        if config_p and config_p.exists():
            with open(config_p, "r") as f:
                config = json.load(f)
    
        id_column =  AnnotatedQueryModel.id
        content_column = AnnotatedQueryModel.query_text

        collection_id = config.get("collection_id", "")
        dataset_name = config.get("dataset_name", "not_referenced")
        
        client_email = config.get("client_email", "admin@example.com")
        client_mdp = config.get("client_mdp", "admin")
        
        client.sign_in(client_email,client_mdp)
        
        model_name = config.get("model_name", "not_referenced")
        
        ollama_client.pull_model(model_name)

        answers = []

        try :
            for i, (df_index, row) in enumerate(
                tqdm(
                    queries.iterrows(),
                    total=queries.shape[0],
                    desc=f"Benchmarking {dataset_name} ({model_name})",
                )
            ):
                query_id = row[id_column]
                query_text = row[content_column]
        
                raw_chat_output = client.chat_with_collection(
                    model_name, query_text, collection_id
                )
        
                model_answer_text, sourced_documents = client.parse_chat_response(
                    raw_chat_output
                )
        
                docs_retrieved = []
                docs_dist = []
                for doc in sourced_documents:
                    docs_retrieved.append(doc.get("name"))
                    docs_dist.append(doc.get("distance"))
        
                
                answer = AnswerModel.model_validate(
                    {
                        "_id": str(uuid.uuid4()),
                        "query": query_text,
                        "model_answer": model_answer_text,
                        "retrieved_documents_ids": docs_retrieved,
                        
                        "retrieved_documents_distances": docs_dist,
                    }
                )
                answers.append(answer)
        
            logging.info("Benchmark terminé.")
            client.delete_collection(collection_id)

        except Exception as e:
            logging.error(
                f"Une erreur est survenue durant le benchmark: {e}", exc_info=True
            )
    
        return answers