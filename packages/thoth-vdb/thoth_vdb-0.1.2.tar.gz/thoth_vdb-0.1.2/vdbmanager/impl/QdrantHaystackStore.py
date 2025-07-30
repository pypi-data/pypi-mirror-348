import logging
from typing import Any, Dict, List, Optional # Added Optional

# Removed os import as API key is no longer needed
from haystack import Pipeline
# Use haystack components import path for SentenceTransformersTextEmbedder
from haystack.components.embedders import SentenceTransformersTextEmbedder # Changed import
from haystack_integrations.components.retrievers.qdrant import QdrantEmbeddingRetriever
from haystack_integrations.document_stores.qdrant import QdrantDocumentStore
from haystack.document_stores.types import DuplicatePolicy

from ..ThothHaystackVectorStore import ThothHaystackVectorStore
from ..ThothVectorStore import (
     BaseThothDocument,
     ThothType,
)


class QdrantHaystackStore(ThothHaystackVectorStore):
    _instances: Dict[tuple, "QdrantHaystackStore"] = {}

    def __new__(cls,
                collection: str,
                host: str = "localhost",
                port: int = 6333,
                api_key: Optional[str] = None): # Added api_key
        instance_key = (collection, host, port, api_key) # Added api_key to instance key
        if instance_key in cls._instances:
            return cls._instances[instance_key]
        
        instance = super().__new__(cls)
        cls._instances[instance_key] = instance
        return instance

    def __init__(self,
                 collection: str,
                 host: str = "localhost",
                 port: int = 6333,
                 api_key: Optional[str] = None): # Added api_key parameter
        # Prevent re-initialization if instance is fetched from cache
        if hasattr(self, '_initialized') and self._initialized:
            return

        # No API key needed for local sentence-transformers

        store = QdrantDocumentStore(
            index=collection,
            host=host,
            port=port,
            api_key=api_key, # Pass api_key
            embedding_dim=384, # Reverted embedding dimension for all-MiniLM-L6-v2
            hnsw_config={
                "m": 16,
                "ef_construct": 100
            }
        )
        super().__init__(store=store, collection_name=collection)
        self._initialized = True # Mark as initialized

    def get_collection_info(self, doc_type: ThothType) -> Dict[str, Any]:
        try:
            client = self.store._client
            collection_info = client.get_collection(self.collection_name)
            points_count = collection_info.points_count
            vectors_config = collection_info.config.params.vectors
            
            return {
                "doc_type": doc_type.value,
                "collection_name": self.collection_name,
                "total_docs": points_count,
                "embedding_dim": vectors_config.size
            }
        except Exception as e:
            logging.error(f"Collection info retrieval failed: {e}")
            return {
                "doc_type": doc_type.value,
                "collection_name": self.collection_name,
                "total_docs": 0,
                "embedding_dim": 384 # Reverted default to match store config
            }

    def search_similar(self,
                       query: str,
                       doc_type: ThothType,
                       top_k: int = 5,
                       score_threshold: float = 0.7) -> List[BaseThothDocument]:
        if not query:
            return []

        # No API key check needed

        try:
            # Use SentenceTransformers embedder
            logging.info("Initializing SentenceTransformersTextEmbedder")
            text_embedder = SentenceTransformersTextEmbedder(
                model="sentence-transformers/all-MiniLM-L6-v2" # Standard ST model
            )
            text_embedder.warm_up() # Call warm_up

            filters = {
                "field": "meta.thoth_type",
                "operator": "==",
                "value": doc_type.value
            }

            retriever = QdrantEmbeddingRetriever(
                document_store=self.store,
                filters=filters,
                top_k=top_k,
                scale_score=True
            )

            pipeline = Pipeline()
            pipeline.add_component("embedder", text_embedder)
            pipeline.add_component("retriever", retriever)
            pipeline.connect("embedder.embedding", "retriever.query_embedding")

            results = pipeline.run({"embedder": {"text": query}})
            thoth_docs = []
            for doc in results["retriever"]["documents"]:
                thoth_doc = self._convert_from_haystack_document(doc)
                if thoth_doc and doc.score >= score_threshold:
                    thoth_docs.append(thoth_doc)

            return thoth_docs

        except Exception as e:
            logging.error(f"Similarity search failed: {e}")
            return []

    # --- Implementation of abstract methods from ThothVectorStore ---

    def _add_document(self, doc: BaseThothDocument) -> str:
        """
        Implements the abstract _add_document method from ThothVectorStore.
        Delegates to the internal add method of the parent Haystack adapter.
        """
        # Use OVERWRITE policy consistent with parent's add_document
        return super()._add_document_internal(doc, policy=DuplicatePolicy.OVERWRITE)

    def get_document(self, doc_id: str) -> Optional[BaseThothDocument]:
        """
        Implements the abstract get_document method from ThothVectorStore.
        Delegates to the get_document_by_id method of the parent Haystack adapter.
        """
        # The parent method already handles conversion and type checking if needed
        # We expect BaseThothDocument here, so no specific output_type is passed.
        return super().get_document_by_id(doc_id=doc_id, output_type=BaseThothDocument)
