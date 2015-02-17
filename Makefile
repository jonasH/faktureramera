uitopythontool=pyuic5


.PHONY tags:
	find . -name "*.py" | etags -

.PHONY all: ui_faktureramera.py ui_jobform.py ui_newcustomerform.py

ui_faktureramera.py: gui/faktureramera.ui
	$(uitopythontool) gui/faktureramera.ui > gui/ui_faktureramera.py

ui_jobform.py: gui/jobform.ui
	$(uitopythontool) gui/jobform.ui > gui/ui_jobform.py

ui_newcustomerform.py: gui/newcustomerform.ui
	$(uitopythontool) gui/newcustomerform.ui > gui/ui_newcustomerform.py

.PHONY static-check:
	pyflakes-check

.PHONY pyflakes-check:
	find . -name "*.py" | xargs pyflakes

.PHONY pep8-check:
	find . -name "*.py" | xargs pep8
