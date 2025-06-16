from typing import List

import google.generativeai as genai


class EmbeddingService:
    def __init__(self, api_key: str = None):
        self.api_key = api_key

        if api_key:
            genai.configure(api_key=api_key)
            print("using gemini")
        else:
            print("Gemini key not provided")

    def embed_text(self, text: str) -> List[float]:
        result = genai.embed_content(
            model="models/embedding-001", content=text, task_type="retrieval_document"
        )
        return result["embedding"]

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        embeddings = []
        for text in texts:
            embeddings.append(self.embed_text(text))
        return embeddings

    def embed_query(self, query: str) -> List[float]:
        """Generate embedding for a query"""

        result = genai.embed_content(
            model="models/embedding-001", content=query, task_type="retrieval_query"
        )
        return result["embedding"]
