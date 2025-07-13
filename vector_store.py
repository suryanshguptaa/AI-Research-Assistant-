import chromadb
from chromadb.config import Settings
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import List, Dict, Any
import os
from config.settings import VECTORSTORE_PERSIST_DIR, COLLECTION_NAME, EMBEDDING_MODEL


class VectorStoreManager:
    """Complete vector store implementation using ChromaDB."""

    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        self.persist_directory = VECTORSTORE_PERSIST_DIR
        self.collection_name = COLLECTION_NAME
        self.vectorstore = None
        self._initialize_vectorstore()

    def _initialize_vectorstore(self):
        """Initialize ChromaDB vector store."""
        try:
            # Ensure directory exists
            os.makedirs(self.persist_directory, exist_ok=True)

            # Initialize ChromaDB client
            client = chromadb.PersistentClient(path=self.persist_directory)

            # Create or get collection
            self.vectorstore = Chroma(
                client=client,
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory
            )

        except Exception as e:
            print(f"Failed to initialize vector store: {e}")
            raise

    def add_document(self, chunks: List[str], metadata: Dict[str, Any]) -> str:
        """Add document chunks to vector store."""
        try:
            # Create documents with metadata
            documents = []
            metadatas = []

            for i, chunk in enumerate(chunks):
                documents.append(chunk)
                chunk_metadata = {
                    **metadata,
                    "chunk_id": i,
                    "chunk_text": chunk[:100] + "..." if len(chunk) > 100 else chunk
                }
                metadatas.append(chunk_metadata)

            # Add to vector store
            self.vectorstore.add_texts(
                texts=documents,
                metadatas=metadatas
            )

            return f"doc_{metadata['filename']}_{len(chunks)}_chunks"

        except Exception as e:
            print(f"Failed to add document to vector store: {e}")
            return None

    def get_vectorstore(self):
        """Return the vector store object."""
        return self.vectorstore

    def get_retriever(self, k: int = 3):
        """Return a retriever object for querying."""
        return self.vectorstore.as_retriever(
            search_kwargs={"k": k}
        )

    def search_documents(self, query: str, k: int = 3):
        """Search for relevant documents."""
        try:
            docs = self.vectorstore.similarity_search(query, k=k)
            return docs
        except Exception as e:
            print(f"Search failed: {e}")
            return []
