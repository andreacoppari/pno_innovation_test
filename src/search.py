import json
from pathlib import Path

from utils import get_vector_store, get_embeddings

from langchain_community.document_loaders import TextLoader

def print_results(docs):
    print(json.dumps(
        [
            {
                "score": float(s),
                "id": getattr(d, "id", None),
                "content": d.page_content,
                "metadata": d.metadata
            } for d,s in docs
        ],
        ensure_ascii=False, indent=2
    ))

def search_index(query: str, k: int = 5) -> None:
    vector_store = get_vector_store()
    embeddings = get_embeddings()
    query = embeddings.embed_query(query)
    docs = vector_store.similarity_search_by_vector_with_relevance_scores(query, k=k)
    print_results(docs)

def load_text(path:str)->str:
    docs = TextLoader(path, encoding="utf-8", autodetect_encoding=True).load()
    return "\n".join(d.page_content for d in docs if d.page_content)

def search_file(path: Path) -> None:
    text = load_text(path)
    embeddings = get_embeddings()
    vectors = embeddings.embed_query(text)
    vector_store = get_vector_store(embeddings)
    docs = vector_store.similarity_search_by_vector_with_relevance_scores(vectors, k=5)
    print_results(docs)