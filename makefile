VENV = .env
PY = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
ACTIVATE = $(VENV)/bin/activate
MAIN = main.py

$(ACTIVATE): requirements.txt
	virtualenv $(VENV)
	$(PIP) install -r requirements.txt

run: $(ACTIVATE)
	$(PY) $(MAIN)

clean: 
	rm -rf __pycache__
	rm -rf $(VENV)

.PHONY: run clean
