import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="HR Knowledge Assistant", layout="wide")
st.title("AI-Powered HR Onboarding Assistant")

# ---------------- SESSION ----------------
if "token" not in st.session_state:
    st.session_state.token = None

# ---------------- TABS ----------------
tab1, tab2 = st.tabs(["Employee Chat", "Admin Dashboard"])

# ---------------- Employee Chat ----------------
with tab1:
    st.header("Ask HR Assistant")

    query = st.text_input("Ask your HR question")

    if st.button("Ask"):
        if query.strip() == "":
            st.warning("Please enter a question.")
        else:
            res = requests.post(f"{BACKEND_URL}/chat", params={"query": query})
            data = res.json()

            st.subheader("Answer")
            st.write(data["answer"])

            st.subheader("Category")
            st.success(data["category"])

            st.subheader("Sources")
            for src in data["sources"]:
                st.info(src)

# ---------------- Admin Dashboard ----------------
with tab2:
    st.header("HR Admin Dashboard")

    # -------- LOGIN --------
    if not st.session_state.token:
        st.subheader("Admin Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            res = requests.post(f"{BACKEND_URL}/login", data={
                "username": username,
                "password": password
            })

            if res.status_code == 200:
                st.session_state.token = res.json()["access_token"]
                st.success("Login successful")
                st.rerun()

            else:
                st.error("Invalid credentials")

    # -------- ADMIN PANEL --------
    else:
        headers = {
            "Authorization": f"Bearer {st.session_state.token}"
        }

        st.success("Logged in as Admin")

        # Logout button
        if st.button("Logout"):
            st.session_state.token = None
            st.rerun()


        # Upload Document
        st.subheader("Upload New Policy Document")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=["pdf", "txt", "docx", "csv", "xlsx", "json"]
        )

        if uploaded_file and st.button("Upload Document"):
            files = {"file": uploaded_file}
            res = requests.post(
                f"{BACKEND_URL}/admin/upload",
                files=files,
                headers=headers
            )

            if res.status_code == 200:
                st.success(res.json()["message"])
            else:
                st.error("Upload failed. Please login again.")

        # List Documents
        st.subheader("Current Knowledge Base Documents")

        res = requests.get(
            f"{BACKEND_URL}/admin/documents",
            headers=headers
        )

        if res.status_code == 200:
            docs = res.json()
            for doc in docs:
                col1, col2 = st.columns([4, 1])
                col1.write(doc)
                if col2.button("Delete", key=doc):
                    requests.delete(
                        f"{BACKEND_URL}/admin/delete/{doc}",
                        headers=headers
                    )
                    st.rerun()

        else:
            st.error("Failed to load documents. Please login again.")
