from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
import shutil
import os

from Backend.Search import RAGSearch
from Backend.VectorStore import FaissVectorStore
from Backend.Data_Loader import load_all_documents
from Backend.auth import authenticate_user, create_access_token, SECRET_KEY, ALGORITHM

# ================= App Setup =================

app = FastAPI(title="HR RAG Assistant")

rag = RAGSearch()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

DATA_DIR = "Data"

# ================= Auth =================

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not authenticate_user(form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    token = create_access_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# ================= Public APIs =================

@app.get("/")
def home():
    return {"message": "HR RAG Assistant is running"}


@app.post("/chat")
def chat(query: str):
    answer, sources = rag.search_and_answer(query)
    category = rag.classify_query(query)

    return {
        "answer": answer,
        "category": category,
        "sources": sources
    }


# ================= Admin APIs (Protected) =================

@app.post("/admin/upload")
async def upload_file(
    file: UploadFile = File(...),
    user=Depends(verify_token)
):
    file_path = os.path.join(DATA_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Rebuild vector DB
    docs = load_all_documents(DATA_DIR)
    store = FaissVectorStore("faiss_store")
    store.build_from_documents(docs)

    return {"message": f"{file.filename} uploaded and indexed successfully"}


@app.get("/admin/documents")
def list_docs(user=Depends(verify_token)):
    return os.listdir(DATA_DIR)


@app.delete("/admin/delete/{filename}")
def delete_doc(filename: str, user=Depends(verify_token)):
    file_path = os.path.join(DATA_DIR, filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        return {"message": "Deleted successfully"}

    return {"error": "File not found"}
