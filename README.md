# PNO Innovation - Semantic Search Tool

A Python CLI for semantic search over a local Chroma vector store using Hugging Face embeddings. Designed for an easy grading experience: install, set-up data, index, and search by query or by a reference file.

## Table of contents

- [Installation](#installation)
- [Usage](#usage)
- [Notebooks](#notebooks)
- [Models & data](#models--data)
- [Used frameworks](#used-frameworks)
- [Future works](#future-works)

## Installation

Requirements:
- Python 3.10 and pip
- make
- curl and unzip

Create the local setup:

```bash
make setup
```

This writes a minimal .env, ensures the Chroma persistence directory exists, downloads the arXiv dataset archive under data/, unpacks it, and produces a 10k subset for quick experiments.

Discover available commands and examples:

```bash
make help
```

## Usage

Index embeddings into a persisting Chroma collection:

```bash
make index
```

Run a semantic search with a text query:

```bash
make search q="A paper about supersymmetry"
```

Run a semantic search using a reference file (find documents similar to the file’s content):

```bash
make search f="example.txt"
```

The search output shows a top match with title, authors, a snippet of the abstract, and a confidence value, followed by other top results with their confidence. It only works with txt files for simplicity, it can be extended to PDFs and online pages via URLs.

## Notebooks

The notebooks folder includes a Jupyter notebook for quick data exploration and further documentation. It demonstrates reading JSONL with pandas, and visualizing distributions with seaborn to understand the dataset before indexing.

## Models & data

Embeddings use a small Sentence Transformers model from Hugging Face that downloads automatically and runs locally without any API key. The dataset is the arXiv metadata collection of abstracts referenced in the assignment and hosted on Kaggle (Cornell University arXiv). The setup step retrieves the archive and prepares a 10k subset to keep iterations fast.

## Used frameworks

LangChain provides a scalable interface across loaders, text splitters, embeddings, retrievers, and vector stores, which makes evolving from a prototype to a larger system straightforward. Chroma is used as the vector store for its tight integration, simple local persistence, and smooth workflow from in-memory tests to a durable local index.

## Future works

- Add a small web service with clean endpoints. A web app (Django/Flask) could expose GET /search?q=\<query\> for text queries and POST /sync to refresh the Chroma collection on a schedule or after a data update. Results would reuse the same formatter shown by the CLI so the API and terminal share one presentation layer.

- Introduce Redis-backed response caching. Cache keys can be the normalized query string or a hash of a reference file’s contents; values are the JSON-serialized ranked results. A short TTL (e.g., 5–10 minutes) keeps responses fresh while cutting repeated embedding and ANN lookups.

- Support result filtering. Expose optional filters like year ranges, categories, or author includes/excludes. In practice, pass metadata filters down to the vector store (where supported) or apply a lightweight post-filter on retrieved candidates before formatting.
