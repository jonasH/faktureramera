#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow

from ui_faktureramera import Ui_MainWindow


class FaktureraMeraWindow(QMainWindow):

    def __init__(self, parent=None):
        """"""
        super(FaktureraMeraWindow, self).__init__(parent)

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    faktureramera = FaktureraMeraWindow()
    faktureramera.show()    
    sys.exit(app.exec_())
