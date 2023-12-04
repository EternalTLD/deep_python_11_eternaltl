.PHONY: all clean test

VENV = venv
REQ_FILE = requirements.txt

all: venv install

venv:
	@python3 -m venv $(VENV)
	@. $(VENV)/bin/activate && pip install --upgrade pip setuptools wheel

install: venv
	@. $(VENV)/bin/activate && python 10/setup.py install
	@. $(VENV)/bin/activate && pip install -r $(REQ_FILE)

test: all
	@. $(VENV)/bin/activate && pytest -s 10/test_cjson.py

clean:
	@rm -rf $(VENV)
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info