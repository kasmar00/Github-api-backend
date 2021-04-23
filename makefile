SHELL := /bin/bash
.PHONY = activate debug clean

run:
	@( \
		source .env/bin/activate; \
		export FLASK_ENV=development; \
		python3 app.py; \
	)

debug:
	@echo "Running with debug variable"
	@( \
		source .env/bin/activate; \
		export FLASK_ENV=development; \
		export flask_debug=true; \
		python3 app.py; \
	)

clean:
	@echo "Cleaning .pyc files"
	@py3clean .

install:
	@echo "Installing dependencies"
	@( \
		source .env/bin/activate; \
		pip install -r requirements.txt; \
	)

env:
	@echo "Creating venv"
	@( \
		python3 -m venv .env
	)