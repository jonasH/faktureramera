#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtSql import QSqlQueryModel
from ui_faktureramera import Ui_MainWindow

import lib.db as db


class FaktureraMeraWindow(QMainWindow):

   def __init__(self,  parent=None):
        """"""
        super(FaktureraMeraWindow, self).__init__(parent)

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    historyModel = QSqlQueryModel()
    if not db.openDatabase():  
        sys.exit(1)


    db.initializeHistoryModel(historyModel)
    faktureramera = FaktureraMeraWindow() 
    faktureramera.ui.tableView.setModel(historyModel)
    faktureramera.show()    

    sys.exit(app.exec_())
