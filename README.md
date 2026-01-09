# 📘 AI-Powered HR Onboarding Assistant (RAG-Based Knowledge System)

An enterprise-grade AI assistant designed to automate HR onboarding support by answering employee questions using company policy documents. The system uses a Retrieval-Augmented Generation (RAG) architecture to ensure accurate, context-aware, and citation-backed answers.
An AI-powered Self-Service HR Knowledge Assistant that allows employees to query company HR policies using natural language.
The system uses **Retrieval-Augmented Generation (RAG)** to provide accurate, context-aware answers backed by policy documents.

---
## 📌 Problem Statement

HR teams spend a significant amount of time answering repetitive questions from new hires regarding:

* Leave policies
* Benefits
* Remote work rules
* Company conduct
* Administrative procedures

This system reduces HR workload by providing a **self-service AI knowledge assistant** that answers employee queries directly from official HR documents.

---

## 🚀 Project Overview

HR teams often spend significant time answering repetitive onboarding questions related to:

* Leave policies
* Benefits
* Code of conduct
* IT & security policies
* Remote work rules

This project solves that problem by building an intelligent HR assistant where:

✔ HR admins upload policy documents
✔ Documents are indexed into a vector database
✔ Employees ask questions in natural language
✔ AI retrieves only relevant policy sections
✔ AI answers with transparent citations

---

## 🏗️ System Architecture

```
Employee / Admin UI (Streamlit)
        |
        |
FastAPI Backend (RAG Engine)
        |
        |
Document Loader → Chunking → Embeddings → FAISS Vector DB
        |
        |
Groq LLM → Answer Generation
```

---

## 📁 Project Folder Structure

```
AI-Powered_HR_Assistant
│
├── Backend
│   ├── main.py              # FastAPI server
│   ├── Search.py            # RAG pipeline logic
│   ├── VectorStore.py       # FAISS vector database
│   ├── Data_Loader.py       # Document ingestion
│   ├── Embeddings.py        # Chunking + embedding pipeline
│   ├── auth.py              # Admin authentication
│
├── Frontend
│   ├── app.py               # Streamlit UI (Employee + Admin)
│
├── Data                    # HR policy documents (PDF, DOCX, TXT, CSV, XLSX, JSON)
│
├── .env.example            # Environment variable template
├── .gitignore              # Prevents secrets and venv upload
├── requirements.txt
└── README.md
```

---

## ⚙️ Tech Stack

| Layer         | Technology            |
| ------------- | --------------------- |
| Frontend      | Streamlit             |
| Backend       | FastAPI               |
| LLM           | Groq LLM              |
| Embeddings    | Sentence Transformers |
| Vector DB     | FAISS                 |
| Auth          | JWT                   |
| RAG Framework | LangChain             |

---

## 🔐 How to Create a Groq API Key

1. Go to 👉 [https://console.groq.com](https://console.groq.com)
2. Sign up using Google/GitHub
3. Navigate to **API Keys**
4. Click **Create API Key**
5. Copy your API key

---

## 🔑 Setup Environment Variables

Create a file named:

```
.env
```

Add inside:

```
GROQ_API_KEY=your_api_key_here
```

⚠️ This file is ignored by Git and will never be uploaded.

---

## 🛠️ Setup Instructions (Run Locally)

### Step 1 — Clone Repository

```bash
git clone https://github.com/Git-Suraj-hub/AI-Powered-HR-Onboarding-Assistant.git
cd AI-Powered-HR-Onboarding-Assistant
```

---

### Step 2 — Create Virtual Environment

```bash
python -m venv RagVenv
```

Activate:

**Windows**

```bash
RagVenv\Scripts\activate
```

**Mac/Linux**

```bash
source RagVenv/bin/activate
```

---

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 4 — Add HR Policy Documents

Place your HR documents inside:

```
Data/
```

Supported formats:

* PDF
* DOCX
* TXT
* CSV
* XLSX
* JSON

---

### Step 5 — Start Backend Server

```bash
uvicorn Backend.main:app --reload
```

Backend runs on:

```
http://localhost:8000
```

---

### Step 6 — Start Frontend (Streamlit)
Open a New Terminal:

```bash
cd Frontend
streamlit run app.py
```

Frontend runs on:

```
http://localhost:8501
```

---

## 🧠 Chunking Strategy

We use **RecursiveCharacterTextSplitter** to break documents into logical chunks:

* Chunk size: 1000 characters
* Overlap: 200 characters
* Separators: Paragraph → Line → Space

This ensures:
✔ Context is preserved
✔ Large documents are searchable
✔ Answers remain accurate

---

## 📦 Vector Database Choice (FAISS)

We use **FAISS** because:

* Fast similarity search
* Works locally (no cloud cost)
* Highly scalable
* Industry-standard vector engine

Embeddings used:

```
all-MiniLM-L6-v2
```

---

## 🔍 How RAG Works

1. HR documents are uploaded
2. Documents are chunked
3. Chunks are embedded into vectors
4. Stored in FAISS database
5. User asks question
6. Similar chunks are retrieved
7. LLM answers strictly from context
8. Source snippets are returned

---


## ⚠️ Current Limitations

1. Only supports English documents
2. No document version history
3. No role-based admin management
4. No cloud deployment (local only)
5. LLM API rate limits depend on provider
6. WhatsApp/Telegram integration not implemented yet

---

## 🔮 Future Improvements

### 1. WhatsApp HR Chatbot Integration

A WhatsApp HR number will be connected to the system.

**Workflow:**

* Employee sends question on WhatsApp
* AI processes question using RAG pipeline
* If answer is found → AI replies instantly
* If answer is not found → forwarded to HR team
* HR reply is logged and added to knowledge base

This enables 24×7 HR support on WhatsApp.

---

### 2. Human-in-the-Loop Escalation

If AI is unsure:

* Ticket created for HR
* HR response is logged
* Knowledge base auto-updated

---

### 3. Multi-Language Support

* Hindi
* Marathi
* Regional languages

---

### 4. Cloud Deployment

* AWS / Azure deployment
* Scalable vector DB
* Load balancing

---

### 5. Analytics Dashboard

* Most asked questions
* HR workload reduction metrics
* Knowledge gaps

---

### 6. Document Versioning

* Track policy changes
* Compare versions
* Audit logs

---

## 📌 Sample Queries

* "How many vacation days do I get?"
* "What is the parental leave process?"
* "Can I work from a coffee shop?"
* "What is the notice period?"

---

## 🏁 Conclusion

This project demonstrates a production-grade **RAG-based enterprise AI system** for HR onboarding automation, delivering:

✔ Accuracy
✔ Transparency
✔ Scalability
✔ Security
✔ Professional architecture

---

## 👨‍💻 Author

**Suraj Singh Mehta**
AI & Software Engineering

---

## ⭐ If you like this project, please star the repository!

---



## 🏆 Summary

This project demonstrates a full-stack, enterprise-ready AI system using modern RAG architecture. It showcases real-world AI engineering, backend development, security, vector search, and user experience design.



## 📌 License

For academic and educational use.



