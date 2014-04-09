#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtSql import QSqlQueryModel, QSqlQuery
from PyQt5.QtCore import pyqtSlot, Qt
from ui_faktureramera import Ui_MainWindow

import lib.db as db
import lib.pdflib as pdflib


class FaktureraMeraWindow(QMainWindow):

   def __init__(self,  parent=None):
        """"""
        super(FaktureraMeraWindow, self).__init__(parent)

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)
        historyModel = QSqlQueryModel()
        self.initializeHistoryModel(historyModel)
        self.ui.tableView.setModel(historyModel)

   @pyqtSlot()
   def on_generateButton_clicked(self):
      idx = self.ui.tableView.selectionModel().currentIndex()
      if idx.row() == -1:
         return
      model = self.ui.tableView.model()
      idx = model.index(idx.row(), 0)
      billId = int(model.data(idx))
      print( billId)
      bill = pdflib.BillGenerator()
      bill.generate()


   def initializeHistoryModel(self, model):
      model.setQuery('select id,reference,bill_date,payed,payed_date from bill')
      model.setHeaderData(0, Qt.Horizontal, "ID")
      model.setHeaderData(1, Qt.Horizontal, "Namn")
      model.setHeaderData(2, Qt.Horizontal, "Fakturan skapad")
      model.setHeaderData(3, Qt.Horizontal, "Betald")
      model.setHeaderData(4, Qt.Horizontal, "Betald Datum")

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    
    if not db.openDatabase():  
        sys.exit(1)

    faktureramera = FaktureraMeraWindow() 
    
    faktureramera.show()    

    sys.exit(app.exec_())
