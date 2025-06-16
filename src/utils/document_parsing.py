from typing import List, Dict
from pathlib import Path


class DocumentProcessor:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def load_markdown_files(self, data_dir: str) -> List[Dict[str, str]]:
        """Load and process markdown files from data directory"""
        documents = []
        data_path = Path(data_dir)

        for file_path in data_path.glob("*.md"):
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                documents.append(
                    {
                        "content": content,
                        "source": str(file_path),
                        "filename": file_path.name,
                    }
                )

        return documents

    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks with overlap"""
        words = text.split()
        chunks = []

        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk_words = words[i : i + self.chunk_size]
            chunk = " ".join(chunk_words)
            chunks.append(chunk)

            if i + self.chunk_size >= len(words):
                break

        return chunks

    def process_documents(
        self, documents: List[Dict[str, str]]
    ) -> List[Dict[str, str]]:
        """Process documents into chunks with metadata"""
        processed_chunks = []

        for doc in documents:
            chunks = self.chunk_text(doc["content"])

            for i, chunk in enumerate(chunks):
                processed_chunks.append(
                    {
                        "text": chunk,
                        "source": doc["source"],
                        "filename": doc["filename"],
                        "chunk_id": f"{doc['filename']}_chunk_{i}",
                    }
                )

        return processed_chunks
