# 🎓 ScholarAI — AI Study & Research Copilot

An AI-powered study assistant that helps students understand and explore their study materials by asking questions directly from PDF documents. ScholarAI combines **Retrieval-Augmented Generation (RAG)**, Gemini embeddings, Groq LLMs, and LangChain to provide context-aware answers through an interactive Streamlit interface.

## ✨ Features

- 📄 **PDF Upload:** Upload PDF documents and process them for question answering.
- 🧠 **Gemini Embeddings:** Convert document chunks into vector representations using Google's Gemini embedding model.
- 🔍 **Semantic Search:** Retrieve relevant passages from uploaded documents using similarity search.
- 💬 **AI Chat Assistant:** Ask questions about your study materials using a Groq-powered language model.
- 📚 **Source References:** Include source filenames and page numbers in document-based answers.
- 🧩 **Context-Aware Responses:** Use retrieved document content to ground answers and reduce unsupported responses.
- 🖥️ **Interactive Interface:** Chat with your documents through a Streamlit web application.
- 🔄 **Conversation Memory:** Maintain conversation context during the active application session.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web interface |
| LangChain | Document processing, embeddings, and agent tools |
| LangGraph | Agent workflow and conversation checkpointing |
| Gemini Embeddings | Document vectorization |
| Groq | Language model inference |
| InMemoryVectorStore | Vector storage and similarity search |
| PyPDFLoader | PDF text extraction |
| RecursiveCharacterTextSplitter | Splitting documents into manageable chunks |
| Python dotenv | Environment variable management |

## 🏗️ How It Works

1. **Upload PDFs:** The user uploads one or more study documents.
2. **Extract Text:** ScholarAI reads the PDF content and page metadata.
3. **Split Documents:** Text is divided into chunks with overlapping content to preserve context.
4. **Generate Embeddings:** Gemini converts document chunks into numerical vectors.
5. **Retrieve Relevant Context:** Similarity search finds passages related to the user's question.
6. **Generate an Answer:** The Groq-powered agent uses retrieved context to formulate a response.
7. **Display Results:** The answer appears in the Streamlit chat interface, with source references when available.

## 🔄 Architecture

```text
PDF Documents
     |
     v
PDF Text Extraction
     |
     v
Text Chunking
     |
     v
Gemini Embeddings
     |
     v
In-Memory Vector Store
     |
     v
Semantic Retrieval Tool
     |
     v
Groq LLM + LangChain Agent
     |
     v
Streamlit Chat Interface
```

## 📁 Project Structure

```text
ScholarAI/
├── apps/
│   └── qna_bot.py
├── data/
│   └── Sample documents (optional)
├── .gitignore
├── requirements.txt
└── README.md
```

The `data/` directory is optional and should contain only documents you are permitted to share publicly. The application can also process PDFs uploaded through the interface.

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/akshayshetty19/ScholarAI.git
cd ScholarAI
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
```

If PowerShell blocks activation, use an appropriate execution policy for your environment or activate the environment from Command Prompt.

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configure API keys

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
```

Get your API keys from:

- [Google AI Studio](https://aistudio.google.com/apikey)
- [Groq Console](https://console.groq.com/keys)

**Security:** Never commit your `.env` file or expose your API keys in source code.

### 5. Run the application

```powershell
python -m streamlit run apps/qna_bot.py
```

Open the local URL displayed in your terminal, usually `http://localhost:8501`.

### 6. Start chatting

1. Upload one or more PDF files.
2. Wait for document processing to finish.
3. Ask questions related to the uploaded documents.
4. Review the generated answers and source references.

## 🔐 Security and Privacy

- Store API keys in environment variables.
- Keep `.env`, virtual environments, and private documents out of Git.
- Review uploaded documents before sharing or publishing them.
- The current vector store uses in-memory storage; document vectors are not persisted between application restarts.

## 🚧 Future Improvements

- [ ] Persistent vector database using ChromaDB
- [ ] Support for document summaries
- [ ] AI-generated quizzes and flashcards
- [ ] Improved source citation and answer verification
- [ ] Evaluation of retrieval relevance and answer quality
- [ ] FastAPI backend for modular API access
- [ ] Persistent document indexing and chat history
- [ ] Streaming responses and improved user experience
- [ ] Support for larger document collections

## 🎯 Project Objective

ScholarAI aims to make learning more interactive and efficient by allowing students to ask questions directly from their study materials instead of manually searching through lengthy documents.

## 👨‍💻 Author

**Akshay Shetty**

GitHub: [@akshayshetty19](https://github.com/akshayshetty19)

---

⭐ If you find this project useful, consider giving the repository a star!
