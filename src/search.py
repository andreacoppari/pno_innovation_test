from typing import List
from pathlib import Path

from utils import get_vector_store, get_embeddings

from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document


def print_results(docs: List[Document]) -> None:
    '''
    docs:   List of langchain.core.Documents of best results from similarity search

    It prints the best result and the others from the top 5.
    '''
    best_doc, best_score = docs[-1]
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
    '''
    query:  Query for semantic search.
    k:      Top k results from the similarity search.

    It performs similarity search of input query over stored embeddings in the persistent Chroma collection.
    '''
    embeddings = get_embeddings()
    vector_store = get_vector_store(embeddings)
    query = embeddings.embed_query(query)
    docs = vector_store.similarity_search_by_vector_with_relevance_scores(query, k=k)
    print_results(docs)


def load_text(path: Path) -> str:
    '''
    path:   File path of "query" reference file.

    It extracts the text from the target reference file chosen for semantic similarity search.

    Returns a string of the file content.
    '''
    docs = TextLoader(path, encoding="utf-8", autodetect_encoding=True).load()
    return "\n".join(d.page_content for d in docs if d.page_content)


def search_file(path: Path, k: int = 5) -> None:
    '''
    path:   File path of "query" reference file.
    k:      Top k results from the similarity search.

    It performs similarity search of input text file (its content) over stored embeddings in the persistent Chroma collection.
    '''
    text = load_text(path)
    embeddings = get_embeddings()
    vectors = embeddings.embed_query(text)
    vector_store = get_vector_store(embeddings)
    docs = vector_store.similarity_search_by_vector_with_relevance_scores(vectors, k=k)
    print_results(docs)