.PHONY: all clean test

VENV = venv
REQ_FILE = requirements.txt

all: venv install

venv:
	@python3 -m venv $(VENV)
	@. $(VENV)/bin/activate && pip install --upgrade pip setuptools wheel

install: venv
	@. $(VENV)/bin/activate && python setup.py install
	@. $(VENV)/bin/activate && pip install -r $(REQ_FILE)

test: all
	@. $(VENV)/bin/activate && pytest -s test_cjson.py
	@. $(VENV)/bin/activate && python3 comparison.py

clean:
	@rm -rf $(VENV)
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info