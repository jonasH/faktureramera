uitopythontool=pyuic5


.PHONY tags:
	find . -name "*.py" | etags -

.PHONY all: ui_faktureramera.py ui_jobform.py ui_newcustomerform.py

ui_faktureramera.py: faktureramera.ui
	$(uitopythontool) faktureramera.ui > ui_faktureramera.py

ui_jobform.py: gui/jobform.ui
	$(uitopythontool) gui/jobform.ui > gui/ui_jobform.py

ui_newcustomerform.py: gui/newcustomerform.ui
	$(uitopythontool) gui/newcustomerform.ui > gui/ui_newcustomerform.py
