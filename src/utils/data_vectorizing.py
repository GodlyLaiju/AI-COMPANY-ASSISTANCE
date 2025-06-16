import chromadb
from typing import List, Dict


class VectorStore:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.client = chromadb.PersistentClient(path=db_path)

        self.collection_name = "company_faq"

        # Get or create collection
        self.collection = self.client.get_or_create_collection(self.collection_name)

    def add_documents(
        self, chunks: List[Dict[str, str]], embeddings: List[List[float]]
    ):
        """Add document chunks and their embeddings to the vector store"""
        ids = [chunk["chunk_id"] for chunk in chunks]
        documents = [chunk["text"] for chunk in chunks]
        metadatas = [
            {"source": chunk["source"], "filename": chunk["filename"]}
            for chunk in chunks
        ]

        self.collection.add(
            embeddings=embeddings, documents=documents, metadatas=metadatas, ids=ids
        )

    def search(self, query_embedding: List[float], k: int = 3) -> Dict:
        """Search for similar documents"""
        results = self.collection.query(query_embeddings=[query_embedding], n_results=k)

        return {
            "documents": results["documents"][0],
            "metadatas": results["metadatas"][0],
            "distances": results["distances"][0],
        }
