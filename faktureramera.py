from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import lib.pdflib as pdflib
 
class FaktureraMera(QWidget):
    def __init__(self, parent=None):
        super(FaktureraMera, self).__init__(parent)
 
        nameLabel = QLabel("Name:")
        self.nameLine = QLineEdit()
        self.submitButton = QPushButton("&Submit")
 
        buttonLayout1 = QVBoxLayout()
        buttonLayout1.addWidget(nameLabel)
        buttonLayout1.addWidget(self.nameLine)
        buttonLayout1.addWidget(self.submitButton)
 
        self.submitButton.clicked.connect(self.submitContact)
 
        mainLayout = QGridLayout()

        mainLayout.addLayout(buttonLayout1, 0, 1)
 
        self.setLayout(mainLayout)
        self.setWindowTitle("Faktureramera")
 
    def submitContact(self):
        bg = pdflib.BillGenerator()
        bg.generate()
 
if __name__ == '__main__':
    import sys
 
    app = QApplication(sys.argv)
 
    screen = FaktureraMera()
    screen.show()
 
    sys.exit(app.exec_())
