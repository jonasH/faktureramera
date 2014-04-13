#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtSql import QSqlQueryModel, QSqlQuery
from PyQt5.QtCore import pyqtSlot, Qt, QDate
from ui_faktureramera import Ui_MainWindow

import lib.db as db
import lib.pdflib as pdflib
import lib.fakturamodel as model

from gui.jobForm import JobForm
from gui.newcustomerform import NewCustomerForm

# TODO: bryt ut denna till en egen klass i gui katalogen
class FaktureraMeraWindow(QMainWindow):

   def __init__(self,  parent=None):
        """"""
        super(FaktureraMeraWindow, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.newCustomer = False
        self.ui.setupUi(self)
        historyModel = QSqlQueryModel()
        self.initializeHistoryModel(historyModel)
        self.ui.tableView.setModel(historyModel)
        job = JobForm()
        self.jobList = [job]
        self.ui.jobsLayout.addWidget(job)
        self.populateCustomers()

   def populateCustomers(self):
      query = QSqlQuery()

      query.exec_('select id, name,address, zipcode from customer')
      while query.next():
         c = self.extractCustomer(query)
         self.ui.customerChooser.addItem(c.name)
         


   @pyqtSlot()
   def on_saveGenerateButton_clicked(self):
      query = QSqlQuery()
      dateFormat = 'yyyy-MM-dd'
      date = QDate.currentDate()
      customerId = self.ui.customerChooser.currentIndex() + 1
      query.exec_('select id, name,address, zipcode from customer where id=' + str(customerId))
      query.next()
      customer = self.extractCustomer(query)
      ## TODO: lägg till ett fält med referens
      bill = model.Bill(1, "ApAN ola", date.toString(dateFormat))
      print (bill.id)
      bill.setCustomer(customer)
      for j in self.jobList:
         text = j.ui.description.text()
         price = int( j.ui.price.text())
         number = int( j.ui.number.text())
         job = model.Job(price,number, text)
         bill.addJob(job)

      #kodduplikat, lägg ut i fun
      pdf = pdflib.BillGenerator(bill)
      if pdf.fileExsists:
         print("file exists")
      else:
         print("file does NOT exist")

      pdf.generate()
      
      
   
   @pyqtSlot()
   def on_addJobButton_clicked(self):
      job = JobForm()
      self.ui.jobsLayout.addWidget(job)
      self.jobList.append(job)
      

   @pyqtSlot()
   def on_removeJobButton_clicked(self):
      if len(self.jobList) == 1:
         return
      job = self.jobList[-1]
      self.ui.jobsLayout.removeWidget(job)
      self.jobList = self.jobList[0:-1]


   @pyqtSlot()
   def on_generateButton_clicked(self):
      idx = self.ui.tableView.selectionModel().currentIndex()
      if idx.row() == -1:
         return

      model = self.ui.tableView.model()
      idx = model.index(idx.row(), 0)
      billId = int(model.data(idx))
      bill = self.getBillData(billId)
      pdf = pdflib.BillGenerator(bill)
      if pdf.fileExsists:
         print("file exists")
      else:
         print("file does NOT exist")

      pdf.generate()

   @pyqtSlot()
   def on_newCustomerButton_clicked(self):
##TODO: det ska gå att ta bort newcustmerform
      if self.newCustomer == True:
         self.ui.newCustomerLayout.removeWidget(self.newCustomerForm)
         self.newCustomer = False
         self.ui.newCustomerButton.setText("Ny")
      else:
         self.newCustomerForm = NewCustomerForm()
         self.ui.newCustomerLayout.addWidget(self.newCustomerForm)
         self.newCustomer = True
         self.ui.newCustomerButton.setText("Ångra")

   def extractBill(self, query):
      id = query.value(0)
      date =query.value(3)
      ref = query.value(2)
      return model.Bill(id,ref,date)


   def extractCustomer(self, query):
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


      query.exec_('select id, c_id, reference, bill_date from bill where id =' + str(billId))
      query.next()

      bill = self.extractBill(query)
      c_id = query.value(1)

      query.exec_('select id, name,address, zipcode from customer where id =' + str(c_id))
      query.next()
      customer = self.extractCustomer(query)
      bill.setCustomer(customer)

      query.exec_('select hours, price,job from jobs where b_id =' + str(bill.id))
      jobs = self.extractJobs(query)
      for j in jobs:
         bill.addJob(j)
      return bill

      
         


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
