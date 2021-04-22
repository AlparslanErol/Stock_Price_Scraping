venv:
	python3 -m pip install --upgrade pip
	python3 -m pip install virtualenv
	python3 -m venv venv

require:
	python3 -m pip install --upgrade pip
	python3 -m pip install -r requirements.txt

clean:
	rm -r venv
	@echo "Cleaning done!"
