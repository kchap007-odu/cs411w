run-demo:
	./demo/start.sh

run-server:
	./start.sh

launch-venv:
	. venv/bin/activate

test:
	python TestDevices.py
	python TestThermostats.py

clean:
	rm -r __pycache__
	rm -r */__pycache__
	rm -r **/__pycache__