from typing import List
import google.generativeai as genai
from src.utils.document_parsing import DocumentProcessor
from src.utils.data_embedding import EmbeddingService
from src.utils.data_vectorizing import VectorStore


class CompanyAssistanceBot:
    def __init__(self, api_key: str = None, chunk_size: int = 500, top_k: int = 3):
        self.api_key = api_key
        self.top_k = top_k

        # Initialize components
        self.doc_processor = DocumentProcessor(chunk_size=chunk_size)
        self.embedding_service = EmbeddingService(api_key=api_key)
        self.vector_store = VectorStore("./chroma_db")

        genai.configure(api_key=api_key)

    def index_documents(self, data_dir: str):
        """Index documents from the data directory"""

        existing = self.vector_store.collection.get()
        if existing.get("ids"):
            print("Vector DB already contains indexed data. Skipping indexing.")
            return

        print("Loading documents...")
        documents = self.doc_processor.load_markdown_files(data_dir)
        print("Documents are loaded ...")

        print("Processing documents into chunks...")
        chunks = self.doc_processor.process_documents(documents)
        print("Processed documents into chunks...")

        print("Generating embeddings...")
        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.embedding_service.embed_batch(texts)

        print("Storing in vector database...")
        self.vector_store.add_documents(chunks, embeddings)

        print(f"Indexed {len(chunks)} chunks from {len(documents)} documents")

    def ask(self, question: str) -> str:
        """Main method to ask a question and get an answer"""
        try:
            query_embedding = self.embedding_service.embed_query(question)

            # Search for relevant chunks
            search_results = self.vector_store.search(query_embedding, k=self.top_k)

            if not search_results["documents"]:
                return "I couldn't find any relevant information in the company policies. Please contact HR for assistance."

            # Generate answer using retrieved context
            answer = self.generate_answer(question, search_results["documents"])

            return answer

        except Exception as e:
            return f"I apologize, but I encountered an error while processing your question: {str(e)}"

    def generate_answer(self, question: str, context_chunks: List[str]) -> str:
        """Generate answer using retrieved context"""
        context = "\n\n".join(context_chunks)
        prompt = f"""You are 'G-Bot', the friendly and knowledgeable guide for employees at GodlyTech Innovations Inc. Your personality is warm, approachable, and professional—like a helpful colleague who knows the company inside and out.

Your purpose is to answer employee questions by interpreting and explaining the provided company policy documents. You are here to make our policies clear and accessible for everyone.

**Company Policy Context:**
{context}

**Employee Question:**
{question}

---

**Your Instructions:**

1.  **Tone and Style:**
    *   Adopt a warm, conversational, and professional tone. Be friendly but not unprofessional.
    *   Start with a friendly greeting.
    *   Use "we" and "our" when talking about GodlyTech to foster a sense of community.

2.  **Explain, Don't Recite:**
    *   **Crucially, do not just copy and paste text from the policy context.**
    *   Your main goal is to *synthesize* the information and explain it clearly in your own words.
    *   Elaborate on the policy, breaking down any complex terms to make them easy to understand. The goal is to sound like a human expert explaining the policy, not a machine retrieving text.

3.  **Infuse a Good Spirit:**
    *   Frame your answers in a positive and supportive way. Help the employee understand how the policy supports them and the company.

4.  **Handling Missing Information:**
    *   If the answer is not found in the provided context, do not invent an answer.
    *   Instead, politely state that you don't have that specific information and suggest the best next step, such as "That's a great question! I don't have the specifics on that in my current documents, but the People & Culture team would be the best resource for an answer," or "You can likely find more details on that in the official employee handbook on the company portal."

---

**Your Helpful Response:**"""
        try:
            model = genai.GenerativeModel("gemini-2.5-flash-preview-04-17")
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"I apologize, but I'm having trouble generating a response right now. Error: {str(e)}"
