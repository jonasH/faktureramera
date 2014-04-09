uitopythontool=pyuic5

ui_faktureramera.py: faktureramera.ui
	$(uitopythontool) faktureramera.ui > ui_faktureramera.py
