setup:
	- python3 -m pip install -r requirements.txt

index:
	- python3 src/main.py index

search:
	- python3 src/main.py search $(q)