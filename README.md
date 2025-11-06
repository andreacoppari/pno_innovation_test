# pno_innovation_test
pno_innovation_test

## CI PENSO
### package
chroma, LangChain, huggingface, redis, "pdfminer" (da langchain), pymongo(?)

### docker?

### logger

## popiline index
1. estraggo testo dal dataset
2. chroma -> vectordb

## popiline search
1. prendo documento/query
2. carico nel vectordb per similarity
3. stampo i 5 documenti più simili con la frase di riferimento nel doc.

### usage

python3 main.py index  // data -> vectordb

python3 main.py search "query" / document.pdf

make index
make search #1

## models
sentence-transformers/all-MiniLM-L6-v2

doc1.pdf doc3.pdf doc2.pdf

doc1.pdf doc4.pdf