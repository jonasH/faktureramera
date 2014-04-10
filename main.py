#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtSql import QSqlQueryModel, QSqlQuery
from PyQt5.QtCore import pyqtSlot, Qt
from ui_faktureramera import Ui_MainWindow

import lib.db as db
import lib.pdflib as pdflib
import lib.fakturamodel as model


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
      self.getBillData(billId)
      return
      bill = pdflib.BillGenerator()
      bill.generate()

   def extractBill(self, query):
      query.next()
      id = query.value(0)
      date =query.value(3)
      ref = query.value(2)
      return model.Bill(id,ref,date)


   def extractCustomer(self, query):
      query.next()
      id =  query.value(0)
      name = query.value(1)
      address = query.value(2)
      zipcode = query.value(3)
      return model.Customer(id,name,address,zipcode)
      

## TODO: hours or number !
   def extractJobs(self,query):
      """"""
      result = []
      while(query.next()):
         price = query.value(1)
         hours = query.value(0)
         text = query.value(2)
         result.append(model.Job(price, hours, text))

      return result

   def getBillData(self,billId):
     #TODO: handle if no record show up
      query = QSqlQuery()
      result = None

      query.exec_('select id, c_id, reference, bill_date from bill where id =' + str(billId))
     
      bill = self.extractBill(query)
      c_id = query.value(1)

      query.exec_('select id, name,address, zipcode from customer where id =' + str(c_id))
      customer = self.extractCustomer(query)
      bill.setCustomer(customer)

      query.exec_('select hours, price,job from jobs where b_id =' + str(bill.id))
      jobs = self.extractJobs(query)
      for j in jobs:
         bill.addJob(j)

      ###TOMORROW: add call to pdf
      

      
         


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
