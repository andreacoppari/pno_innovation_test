from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from dotenv import load_dotenv
import os

def get_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def get_vector_store(embeddings = get_embeddings()):
    load_dotenv()
    return Chroma(
        collection_name=os.getenv("COLLECTION"),
        embedding_function=embeddings,
        persist_directory=os.getenv("PERSIST_DIR"),
    )
