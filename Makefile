venv:
	python -m pip install --user --upgrade pip
	python -m pip install --user virtualenv
	python -m venv venv

require:
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt

clean:
	rm -r venv
	@echo "Cleaning done!"
