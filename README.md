````markdown
# Company AI Chatbot (Gradio + RAG)

A conversational chatbot UI built with Gradio that lets users interact with your company’s AI knowledge base, powered by Retrieval-Augmented Generation (RAG) using Google Gemini embeddings and ChromaDB.

---

## 🚀 Features

- **Retrieval-Augmented Generation**  
  • Indexes your company policy/docs as chunks in a vector store  
  • On-demand retrieval of relevant context for each user query  
  • Golden‑tone “G‑Bot” persona for friendly, professional responses  

- **Gradio Chat Interface**  
  • Simple, web‑based chat UI  
  • “Share” mode for public demos  
  • Customizable theme and layout  

- **Modular & Extensible**  
  • Pluggable document parsers, embedding services, and vector stores  
  • Add new document types (PDF, Word) or switch embedding providers  
  • Easily adjust chunk size, overlap, and number of retrieved results  

---

## 📦 Prerequisites

- Python 3.10+  
- Google Gemini API Key (for embeddings & generation)  
- `chromadb` (for vector database)  
- A folder of Markdown (or other) policy/docs under `./source_data`

---

## 🔧 Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/your-org/company-ai-chatbot.git
   cd company-ai-chatbot
````

2. **Create & activate a virtual environment**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   .venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set your environment variables**
   Create a `.env` file in project root:

   ```env
   GEMINI_API_KEY=your_google_gemini_api_key_here
   ```

---

## 🗂️ Project Structure

```
.
├── .env
├── main.py                   # Entry point: sets up Gradio and bot initialization
├── requirements.txt          # Python dependencies
├── src/
│   ├── ai_assistance.py      # CompanyAssistanceBot: RAG orchestration
│   ├── document_parsing.py   # DocumentProcessor: load & chunk markdown files
│   ├── data_embedding.py     # EmbeddingService: Google Gemini embedding calls
│   ├── data_vectorizing.py   # VectorStore: chromadb storage & search
│   └── utils/                # (Optional) helper modules
│       └── ...
├── source_data/              # Your company policy/docs (Markdown files)
│   └── *.md
└── README.md
```

---

## ⚙️ Configuration

| Setting         | Location               | Description                                                |
| --------------- | ---------------------- | ---------------------------------------------------------- |
| `chunk_size`    | `CompanyAssistanceBot` | Max words per chunk (default: 500)                         |
| `chunk_overlap` | `DocumentProcessor`    | Overlap between chunks (default: 50)                       |
| `top_k`         | `CompanyAssistanceBot` | Number of top documents to retrieve per query (default: 3) |
| `theme`         | `gr.ChatInterface`     | Gradio theme (e.g., `ocean`, `default`)                    |
| `share`         | `.launch(share=True)`  | Whether to enable Gradio’s public share link               |

---

## 🚀 Usage

1. **Prepare your documents**
   Place all your Markdown policy/docs in `./source_data/`.
   Example:

   ```
   source_data/
   ├── Employee_Handbook.md
   ├── Code_of_Conduct.md
   └── IT_Policies.md
   ```

2. **Index documents**
   On first run, the bot will automatically chunk, embed, and store vectors in `./chroma_db/`.

   ```bash
   python main.py
   ```

   You should see console logs:

   ```
   Initializing FAQ Bot...
   Loading documents...
   Processing documents into chunks...
   Generating embeddings...
   Storing in vector database...
   Indexed 150 chunks from 5 documents
   ```

3. **Chat with G‑Bot!**
   After successful indexing, Gradio will launch a local web UI.

   * **Local:** `http://127.0.0.1:7860/`
   * **Share Link:** As printed in the console

4. **Ask questions**
   💬 “What’s our PTO policy?”
   💬 “How do I reset my corporate VPN password?”

---

## 📈 How it Works

1. **Document Parsing**

   * `DocumentProcessor` loads each `.md` file and splits text into overlapping chunks.
2. **Embedding Generation**

   * `EmbeddingService` calls Google Gemini to convert text chunks (and user queries) into high‑dimensional vectors.
3. **Vector Store**

   * `VectorStore` (ChromaDB) indexes embeddings & metadata for fast similarity search.
4. **RAG Workflow**

   * On each user query:

     1. Embed the question
     2. Retrieve top‑k relevant chunks
     3. Feed context + question into the Gemini generative model
     4. Return a coherent, policy‑aware answer

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/awesome`)
3. Commit your changes (`git commit -m "Add awesome feature"`)
4. Push (`git push origin feature/awesome`)
5. Open a Pull Request

Please follow the existing code style and write tests for new functionality.

---

*Happy chatting with your Company AI! 🎉*

```
```
