import io
import uuid
import streamlit as st
import PyPDF2
from sentence_transformers import SentenceTransformer
from endee import Endee
import json

# Page config
st.set_page_config(page_title="Resume Analyzer", layout="wide")

INDEX_NAME = "resumes"
DIMENSION = 384
TOP_K = 5


# Load embedding model
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


# Connect to Endee (FIXED VERSION)
@st.cache_resource
def init_endee():
    client = Endee("localhost:8080")

    try:
        indexes = client.list_indexes()

        # Handle different response formats
        if isinstance(indexes, str):
            indexes = json.loads(indexes)

        if isinstance(indexes, dict):
            indexes = indexes.get("indexes", [])

        names = [i["name"] for i in indexes] if indexes else []

    except Exception as e:
        raise Exception(f"Cannot connect to Endee: {e}")

    if "resumes" not in names:
        client.create_index(
            name="resumes",
            dimension=384,
            space_type="cosine"
        )

    return client.get_index("resumes")


# Extract text from PDF
def extract_text(file_bytes):
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content
    return text


# Generate embedding
def embed(model, text):
    return model.encode(text).tolist()


# UI
st.title("Resume Analyzer")
st.write("Upload resumes and match them with a job description using semantic search.")


# Load model
with st.spinner("Loading model..."):
    model = load_model()


# Connect Endee
try:
    index = init_endee()
    st.success("Connected to Endee")
except Exception as e:
    st.error(f"Endee connection failed:\n{e}")
    st.stop()


# Upload resumes
uploaded_files = st.file_uploader(
    "Upload resumes (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    if st.button("Index Resumes"):
        with st.spinner("Processing resumes..."):
            vectors = []

            for file in uploaded_files:
                text = extract_text(file.read())

                if not text.strip():
                    st.warning(f"Skipping {file.name} (no text found)")
                    continue

                vector = embed(model, text)

                vectors.append({
                    "id": str(uuid.uuid4()),
                    "vector": vector,
                    "meta": {"name": file.name}
                })

            if vectors:
                index.upsert(vectors)
                st.success(f"{len(vectors)} resumes indexed")


# Job description
jd = st.text_area("Enter Job Description")

if st.button("Find Matches"):
    if not jd.strip():
        st.warning("Please enter a job description")
        st.stop()

    with st.spinner("Searching..."):
        query_vec = embed(model, jd)
        results = index.query(vector=query_vec, top_k=TOP_K)

    if not results:
        st.info("No resumes found")
    else:
        st.subheader("Top Matches")

        for i, r in enumerate(results, 1):
            name = r.get("meta", {}).get("name", "Unknown")
            score = round(r.get("similarity", 0) * 100, 2)

            st.write(f"{i}. {name} - {score}% match")
