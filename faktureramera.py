from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import lib.pdflib as pdflib
 
class FaktureraMera(QWidget):
    def __init__(self, parent=None):
        super(FaktureraMera, self).__init__(parent)
        settingsWidget = SettingsWidget(parent=self)

        table = QTableView(self)

        tabPane = QTabWidget(self)

        tabPane.addTab(table, "Fakturera")
        tabPane.addTab(table, "History")
        tabPane.addTab(settingsWidget, "Settings")
        
        tabLayout = QVBoxLayout()
        tabLayout.addWidget(tabPane)
        
        
        mainLayout = QGridLayout()

        mainLayout.addLayout(tabLayout, 0, 1)
        
 
        self.setLayout(mainLayout)
        self.setWindowTitle("Faktureramera")
 
    def submitContact(self):
        bg = pdflib.BillGenerator()
        bg.generate()
 


class SettingsWidget(QWidget):
    def __init__(self, parent=None):
        super(SettingsWidget, self).__init__(parent)
        nameLine = QTextEdit()
        layout = QVBoxLayout()
        layout.addWidget(nameLine)
        self.setLayout(layout)
        

# class HistoryWidget(QWidget):
#     pass

# class BillingWidget(QWidget):
#     pass

if __name__ == '__main__':
    import sys
 
    app = QApplication(sys.argv)
 
    screen = FaktureraMera()
    screen.show()
 
    sys.exit(app.exec_())
