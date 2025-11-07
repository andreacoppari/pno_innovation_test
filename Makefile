
Y:=\033[33m
G:=\033[32m
C:=\033[36m
R:=\033[31m
B:=\033[34m
N:=\033[0m

.PHONY: help setup search index clean

help:
	@echo "$(Y)--------------------------------------------$(N)"
	@echo "$(Y)🚀 PNO Innovation - Semantic Search Tool$(N)"
	@echo "$(Y)--------------------------------------------$(N)"
	@echo "Use $(Y)make setup$(N) to install python dependencies, then use $(Y)make index$(N) to index the dataset. Use $(R)make clean$(N) to cleanup the working directory from data"
	@echo ""
	@echo "$(G)Search usage$(N):"
	@echo "  $(Y)make search f=\"A paper about supersymmetry\"$(N)"
	@echo "  $(Y)make search f=\"example.txt\"$(N)"
	@echo "$(Y)------------------------------------------------$(N)"

setup:
	@echo "A paper about supersymmetry" > example.txt
	@python3 -m pip install -qU -r requirements.txt
	@echo "$(C)[setup]$(N) Running src/setup.py"
	@python3 src/setup.py

search:
	@test -n "$(f)" || (echo "$(R)Error: provide a query or a file path via f=<query>$(N)"; exit 1)

	@echo "$(C)[search]$(N) $(Y)$(f)$(N)"
	@python3 src/main.py search "$(f)"

index:
	@echo "$(C)[index] Loading embdeddings...$(N)"
	@python3 src/main.py index

clean:
	@if [ -d "data/" ]; then \
		echo "$(R)[clean] Removing data/ directory$(N)"; \
		rm -rf -- "data/"; \
	else \
		echo "$(Y)[clean] Nothing to remove at data/$(N)"; \
	fi