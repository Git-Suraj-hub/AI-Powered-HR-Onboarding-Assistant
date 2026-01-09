import os
from dotenv import load_dotenv
from Backend.VectorStore import FaissVectorStore
from Backend.Data_Loader import load_all_documents
from langchain_groq import ChatGroq

load_dotenv()


class RAGSearch:
    def __init__(
        self,
        persist_dir: str = "faiss_store",
        embedding_model: str = "all-MiniLM-L6-v2",
        llm_model: str = "openai/gpt-oss-120b"
    ):
        # Load Vector Store
        self.vectorstore = FaissVectorStore(persist_dir, embedding_model)

        faiss_path = os.path.join(persist_dir, "faiss.index")
        meta_path = os.path.join(persist_dir, "metadata.pkl")

        if not (os.path.exists(faiss_path) and os.path.exists(meta_path)):
            print("[INFO] Building vector store from documents...")
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            DATA_DIR = os.path.join(BASE_DIR, "Data")

            docs = load_all_documents(DATA_DIR)

            if len(docs) == 0:
                raise ValueError("No HR documents found in Data folder.")

            self.vectorstore.build_from_documents(docs)
        else:
            print("[INFO] Loading existing vector store...")
            self.vectorstore.load()

        # Load API Key
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")

        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not found in .env file")

        # Initialize LLM
        self.llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name=llm_model
        )

        print(f"[INFO] Groq LLM initialized: {llm_model}")

    # ================= HR Answer Generation =================

    def search_and_answer(self, query: str, top_k: int = 5):
        results = self.vectorstore.query(query, top_k=top_k)

        if not results:
            return "I don't know based on the available HR policies.", []

        context_blocks = []
        sources = []

        for r in results:
            meta = r["metadata"]
            text = meta["text"]
            source_file = meta.get("source", "HR Policy")
            page = meta.get("page", "N/A")
            full_path = meta.get("full_path", "")

            context_blocks.append(text)

            clean_snippet = " ".join(text.split())[:180] + "..."

            sources.append({
                "document": source_file,
                "page": page,
                "snippet": clean_snippet,
                "path": full_path
            })

        context = "\n\n".join(context_blocks)

        if not context.strip():
            return "I don't know based on the available HR policies.", []

        prompt = f"""
    You are an AI-powered Human Resources (HR) Assistant for a corporate organization.

    Your responsibility is to provide employees with accurate, professional, and policy-compliant information.

    Strict Rules:
    1. You must answer strictly and only from the provided HR policy context.
    2. Do not use external knowledge or assumptions.
    3. If the answer is not found in the context, respond exactly with:
       "I don't know based on the available HR policies."
    4. Do not provide legal advice or personal opinions.
    5. Maintain a professional, respectful, and neutral tone.
    6. Do not speculate or guess.
    7. Do not expose internal system logic.

    If the question involves:
    - Salary disputes
    - Termination
    - Harassment
    - Legal matters
    - Compliance issues

    Then respond:
    "Please contact the HR department for further assistance on this matter."

    Context:
    {context}

    Employee Question:
    {query}

    HR Response:
    """

        response = self.llm.invoke(prompt)
        return response.content.strip(), sources

    # ================= HR Query Classification =================

    def classify_query(self, query: str):
        prompt = f"""
You are an HR domain expert.

Classify the following employee question into exactly one of these categories:

- Benefits
- Leave
- Legal
- IT Policy
- Culture
- Payroll
- Compliance

Return only the category name. Do not add explanations.

Employee Question:
{query}

Category:
"""

        response = self.llm.invoke(prompt)
        return response.content.strip()


# ================= Test =================

if __name__ == "__main__":
    rag_search = RAGSearch()

    query = "How can I resign from this job?"
    answer, sources = rag_search.search_and_answer(query)

    print("\nAnswer:\n", answer)
    print("\nSources:")
    for src in sources:
        print("-", src)
