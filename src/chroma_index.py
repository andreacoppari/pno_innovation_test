import json
import os

from pathlib import Path
from datetime import datetime

from tqdm import tqdm

from utils import get_vector_store, get_embeddings

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

embeddings = get_embeddings()

vector_store = get_vector_store()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=120,
    separators=["\n\n", "\n", ". ", " "],
)

def parse_year(update_date: str | None) -> int | None:
    '''
    update_date: Date string in "yyyy-mm-gg" format.

    Returns the year of the update_date, useful for implementations of filters later on.
    '''
    try:
        return datetime.fromisoformat(update_date).year
    except Exception:
        return None

def normalized_authors(raw_authors: str | list | None) -> str:
    '''
    raw_authors: List of authors parsed (if present) or not

    Returns a normalized list of strings.
    '''
    if isinstance(raw_authors, list):
        return ", ".join([" ".join([p for p in parts if p]).strip() for parts in raw_authors])
    if isinstance(raw_authors, str):
        return [a.strip() for a in raw_authors.split(",")]
    return []

def paper_to_documents(paper: dict) -> list[Document]:
    '''
    paper: The paper object from the dataset

    Returns a list of langchain.core.Document objects that can be stored in a vector db such as Chroma.
    Those objects contain chunks of papers' abstracts, that will be later retrieved using semantic similarity.
    Each object has its unique id composed of <arxiv_id>:<chunk_id>
    '''
    text = (paper.get("abstract") or "").strip()
    if not text:
        return []

    chunks = splitter.split_text(text)

    authors = normalized_authors(paper.get("authors_parsed") or paper.get("authors"))
    categories = paper.get("categories") or ""
    year = parse_year(paper.get("update_date"))
    base_id = paper.get("id")

    docs = []
    for idx, chunk in enumerate(chunks):
        docs.append(
            Document(
                page_content=chunk,
                metadata={
                    "arxiv_id": base_id,
                    "title": paper.get("title"),
                    "authors": authors,
                    "all_categories": categories,
                    "doi": paper.get("doi"),
                    "journal_ref": paper.get("journal-ref"),
                    "update_date": paper.get("update_date"),
                    "year": year,
                    "version_count": len(paper.get("versions") or []),
                    "source": "arxiv",
                    "chunk_index": idx,
                    "total_chunks": len(chunks),
                },
                id=f"{base_id}:{idx}",
            )
        )
    return docs

def index_dataset(path: str):
    
    Path(os.getenv("PERSIST_DIR")).mkdir(parents=True, exist_ok=True)

    with open(path, "r", encoding="utf-8") as fp:
        batch_docs = []
        for line in tqdm(fp, desc="Indexing documents...", total=10000):
            paper = json.loads(line)
            docs = paper_to_documents(paper)
            if not docs:
                continue
            batch_docs.extend(docs)
            if len(batch_docs) >= 256:
                vector_store.add_documents(documents=batch_docs)
                batch_docs = []
        if batch_docs:
            vector_store.add_documents(documents=batch_docs)

