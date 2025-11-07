from typing import List
from pathlib import Path

from utils import get_vector_store, get_embeddings

from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document

def print_results(docs: List[Document]):
    best_doc, best_score = docs[-1]
    md = best_doc.metadata or {}
    print(f'Best result: \t{best_doc.metadata["title"]}')
    print(f'Confidence: \t{best_score:.3f}')
    print(f'Authors: \t{best_doc.metadata["authors"]}')
    print(f'Abstract:\n{best_doc.page_content}')
    print()

    if len(docs) > 1:
        print("Other results:")
        for doc, score in docs[-2::-1]:
            print(f'- {doc.metadata["title"]} | Score: {score:.3f}')

def search_index(query: str, k: int = 5) -> None:
    vector_store = get_vector_store()
    embeddings = get_embeddings()
    query = embeddings.embed_query(query)
    docs = vector_store.similarity_search_by_vector_with_relevance_scores(query, k=k)
    print_results(docs)

def load_text(path:str)->str:
    docs = TextLoader(path, encoding="utf-8", autodetect_encoding=True).load()
    return "\n".join(d.page_content for d in docs if d.page_content)

def search_file(path: Path, k: int = 5) -> None:
    text = load_text(path)
    embeddings = get_embeddings()
    vectors = embeddings.embed_query(text)
    vector_store = get_vector_store(embeddings)
    docs = vector_store.similarity_search_by_vector_with_relevance_scores(vectors, k=k)
    print_results(docs)