import sys
import subprocess
import os

from tqdm import tqdm
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ZIP = DATA / "arxiv.zip"
JSONL = DATA / "dataset.jsonl"
OUT_JSON = DATA / "dataset_10k.json"
OUT_JSONL = DATA / "dataset_10k.jsonl"

def sh(cmd: list[str]):
    subprocess.check_call(cmd)

def main():

    # Normally I would secure the .env file on S3
    with open(".env", "w") as fp:
        fp.write(
            'COLLECTION="Abstracts"\n' \
            'PERSIST_DIR="./data/chroma_db"'
            )

    DATA.mkdir(parents=True, exist_ok=True)

    if not os.path.exists(JSONL):
        url = "https://www.kaggle.com/api/v1/datasets/download/Cornell-University/arxiv"
        print(f"[setup] downloading -> {ZIP}")
        sh(["curl", "-L", "-o", str(ZIP), url])

    print(f"[setup] unzipping -> {DATA}")
    sh(["unzip", "-o", str(ZIP), "-d", str(DATA)])

    print(f"[setup] removing {ZIP}...")
    sh(["rm", str(ZIP)])

    src = DATA / "arxiv-metadata-oai-snapshot.json"
    if src.exists():
        print(f"[setup] renaming {src.name} -> {JSONL.name}")
        if JSONL.exists():
            JSONL.unlink()
        src.rename(JSONL)
    else:
        print("[setup] ERROR: arxiv-metadata-oai-snapshot.json not found after unzip", file=sys.stderr)
        sys.exit(1)

    print(f"[setup] creating 10k subsets -> {OUT_JSON} , {OUT_JSONL}")
    dataset_10k_jsonl = []
    with open(JSONL, "r", encoding="utf-8") as fp:
        for i, line in enumerate(tqdm(fp, desc="Loading dataset entries", total=10000)):
            if i < 10000:
                dataset_10k_jsonl.append(line)
            else:
                break

    with open(OUT_JSONL, "w", encoding="utf-8") as fout:
        for line in dataset_10k_jsonl:
            fout.write(line)

    print("[setup] done")

if __name__ == "__main__":
    main()
