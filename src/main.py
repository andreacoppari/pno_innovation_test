import argparse
import os.path

from pathlib import Path

from search import search_file, search_index
from chroma_index import index_dataset

def main():
    parser = argparse.ArgumentParser(description="PNO Innovation - Semantic Search Tool")
    sub = parser.add_subparsers(dest="command", required=True)

    p_index = sub.add_parser("index", help="Index data into vectordb")
    p_index.add_argument("data", nargs="?", default=None)

    p_search = sub.add_parser("search", help="Search indexed corpus")
    p_search.add_argument("query", type=str)

    args = parser.parse_args()

    if args.command == "index":
        index_dataset("data/dataset_10k.jsonl")
    elif args.command == "search":
        if os.path.exists(args.query):
            search_file(Path(args.query))
        else:
            search_index(args.query)

if __name__ == "__main__":
    main()
