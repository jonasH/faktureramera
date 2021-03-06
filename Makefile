CONFIGFILE=config/config.toml
ALL_FOLDERS=src test/integration_tests test/e2e
ALL_FILES=$(shell find $(ALL_FOLDERS) -name ".*" -prune -o -name "*.py" -print)
.PHONY: test check mypy flake8 format clean exe integration-test

default: src/ui/faktureramera.py src/ui/i18n/en_US.qm src/ui/i18n/se_SE.qm


# Generic project
build:
	mkdir build

clean:
	rm -rf build dist


format:
	black $(ALL_FOLDERS)


TAGS: $(ALL_FILES)
	etags $(ALL_FILES)


# Static checks
check: mypy flake8

build/flake8-report.txt: build $(ALL_FILES)
	rm -f $@ && flake8 --config $(CONFIGFILE) $(ALL_FILES) --output-file=$@ --tee

flake8: build/flake8-report.txt

mypy:
	mypy --config-file $(CONFIGFILE) $(ALL_FOLDERS)

# Testing
COVERAGE_FLAGS=--branch --source=ui,domain,ext -p -m pytest

test: build/coverage.xml

build/coverage.xml: build integration-test e2etest unittest
	cd src && coverage combine && coverage xml -o ../$@ && coverage report --show-missing && cp .coverage ../


integration-test: $(ALL_FILES) build
	cd src && coverage run $(COVERAGE_FLAGS) --junitxml=../build/integration_test_result.xml ../test/integration_tests  

e2etest: $(ALL_FILES) build
	cd src && coverage run $(COVERAGE_FLAGS) --junitxml=../build/e2e_test_result.xml ../test/e2e

unittest: $(ALL_FILES) build
	cd src && coverage run $(COVERAGE_FLAGS) --junitxml=../build/unit_test_result.xml ../test/unit

# qt

src/ui/faktureramera.py: src/ui/faktureramera.ui
	pyside2-uic $< > $@ && sed -i 's/\(.*QCoreApplication.translate("MainWindow", \)u\([^,]*\), None\(.*\)/\1\2\3/g' $@



src/ui/i18n: src/ui/i18n/en_US.qm src/ui/i18n/se_SE.qm

src/ui/i18n/en_US.qm: src/ui/i18n/en_US.ts
	lrelease-qt5 $<

src/ui/i18n/se_SE.qm: src/ui/i18n/se_SE.ts
	lrelease-qt5 $<

GUI_FILES=src/ui/faktureramera.py src/ui/faktureramerawindow.py src/ui/jobform.ui src/ui/newcustomerform.ui

src/ui/i18n/en_US.ts: $(GUI_FILES)
	pyside2-lupdate $^ -ts $@

src/ui/i18n/se_SE.ts: $(GUI_FILES)
	pyside2-lupdate $^ -ts $@

# Installer
exe: clean
	pyinstaller config/FaktureraMera.spec

