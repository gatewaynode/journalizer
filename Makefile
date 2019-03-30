clean:
	find . -name '*.py[co]' -delete

virtualenv:
	virtualenv --prompt '>>- Journalizer -<< ' --python=python3 env
	env/bin/pip install -r requirements.txt
	@echo
	@echo "VirtualENV Setup Complete. Now run: source env/bin/activate"
	@echo

test:
	python -m pytest \
		-v \
		--cov=journalizer \
		--cov-report=term \
		--cov-report=html:coverage-report \
		tests/
build:
	pyinstaller --onefile journalizer.py
install:
	if [ -f "~/.local/bin/jo" ]; then rm -rf ~/.local/bin/jo; fi
	cp dist/journalizer ~/.local/bin/jo
	if [ -d "build" ]; then rm -rf build; fi
	if [ -d "dist" ]; then rm -rf dist; fi
