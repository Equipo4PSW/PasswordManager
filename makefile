VENV = .env
PY = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
ACTIVATE = $(VENV)/bin/activate
MAIN = pm.py

$(ACTIVATE): requirements.txt
	virtualenv $(VENV)
	$(PIP) install -r requirements.txt

run: $(ACTIVATE)
	$(PY) $(MAIN)

h: $(ACTIVATE)
	$(PY) $(MAIN) --help

cldata:
	rm -rf data

clean: 
	rm -rf $(VENV)
	rm -rf data
	find . -type d -name "__pycache__" -exec rm -rf {} +

.PHONY: run clean
