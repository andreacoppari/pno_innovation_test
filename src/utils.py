from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from dotenv import load_dotenv
import os

def get_embeddings() -> HuggingFaceEmbeddings:
    '''
    No parameters

    Returns embeddings for Chroma vector store.
    '''
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def get_vector_store(embeddings : HuggingFaceEmbeddings = get_embeddings()) -> Chroma:
    '''
    embeddings: Load HF embeddings. Use this parameter if the embeddings are already in memory.

    Returns a Chroma vector store, constants are loaded from the .env file.
    '''
    load_dotenv()
    return Chroma(
        collection_name=os.getenv("COLLECTION"),
        embedding_function=embeddings,
        persist_directory=os.getenv("PERSIST_DIR"),
    )
