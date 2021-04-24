SHELL := /bin/bash
.PHONY = run debug clean check install env

run:
	@( \
		source .env/bin/activate; \
		export FLASK_ENV=development; \
		python3 wsgi.py; \
	)

debug:
	@echo "Running with debug variable"
	@( \
		source .env/bin/activate; \
		export FLASK_ENV=development; \
		export flask_debug=true; \
		python3 wsgi.py; \
	)

clean:
	@echo "Cleaning .pyc files"
	@py3clean .

check:
	@echo "Run tests"
	@( \
		source .env/bin/activate; \
		python3 -m test.test_resources;\
	)

install:
	@echo "Installing dependencies"
	@( \
		source .env/bin/activate; \
		pip install -r requirements.txt; \
	)

env:
	@echo "Creating venv"
	@( \
		python3 -m venv .env \
	)