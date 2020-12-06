.PHONY: init
init:
	pip install -r requirements.txt

dev:
	pip install -r requirements-dev.txt

test:
	pytest --html=./tests_coverage/report.html --cov-report html --cov=pyfenstein3d tests/

report-test-result:
	"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" .\tests_coverage\report.html

report-test-coverage:
	"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" .\tests_result\index.html