CONFIGFILE=config/config.toml

ALL_FILES=$(shell find src -name "*.py")
COVERAGE_FLAGS=--branch --source=ui,domain,ext -m pytest
COVERAGE_REPORT_CMD=coverage report --show-missing && cp .coverage ../
.PHONY: test check mypy flake8 format clean exe

clean:
	rm -rf build dist

check: mypy flake8

flake8:
	flake8 --config $(CONFIGFILE) src
mypy:
	mypy --config-file $(CONFIGFILE) src

test:
	cd src && coverage run $(COVERAGE_FLAGS) ../test/integration_tests && $(COVERAGE_REPORT_CMD)
e2etest:
	cd src && coverage run $(COVERAGE_FLAGS) ../test/e2e && $(COVERAGE_REPORT_CMD)

format:
	black src test

TAGS: $(ALL_FILES)
	etags $(ALL_FILES)

exe: clean
	pyinstaller config/FaktureraMera.spec
