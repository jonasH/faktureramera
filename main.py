#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow,QErrorMessage
from PyQt5.QtSql import QSqlQueryModel, QSqlQuery
from PyQt5.QtCore import pyqtSlot, Qt, QDate
from ui_faktureramera import Ui_MainWindow

import lib.db as db
import lib.pdflib as pdflib
import lib.fakturamodel as model

from gui.jobForm import JobForm
from gui.newcustomerform import NewCustomerForm

import os
import webbrowser
    
# TODO: bryt ut denna till en egen klass i gui katalogen
class FaktureraMeraWindow(QMainWindow):

   def __init__(self,  parent=None):
        """"""
        super(FaktureraMeraWindow, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.newCustomerActivated = False
        self.ui.setupUi(self)
        historyModel = QSqlQueryModel()
        self.initializeHistoryModel(historyModel)
        self.ui.tableView.setModel(historyModel)
        job = JobForm()
        self.jobList = [job]
        self.ui.jobsLayout.addWidget(job)
        self.populateCustomers()
        self.newCustomerForm = NewCustomerForm()
        self.newCustomerForm.hide()
        self.ui.newCustomerLayout.addWidget(self.newCustomerForm)

   def populateCustomers(self):
      query = QSqlQuery()
      self.ui.customerChooser.clear()
      query.exec_('select id, name,address, zipcode from customer')
      while query.next():
         c = self.extractCustomer(query)
         self.ui.customerChooser.addItem(c.name)
         
#TODO: move to db
   def newBill(self, reference, cId):
      """"""
      dateFormat = 'yyyy-MM-dd'
      date = QDate.currentDate()
      query = QSqlQuery()
      sql = "insert into bill values((select max(id) from bill) + 1,'{0}','{1}','{2}',0,NULL)".format(cId, reference,date.toString(dateFormat))
      query.exec_(sql)
      query.exec_('select id, c_id, reference, bill_date from bill order by id desc limit 1')
      query.next()
      return self.extractBill(query)

   def newCustomer(self,name, address, zip):
      query = QSqlQuery()
      sql = "insert into customer values((select max(id) from customer) + 1,'{0}','{1}','{2}')".format(name,address, zip)
      query.exec_(sql)
      query.exec_('select id, name,address, zipcode from customer order by id desc limit 1')
      query.next()
      return self.extractCustomer(query)


   def newJob(self,price,number, text,bId):
      query = QSqlQuery()
      sql = "insert into jobs values((select max(id) from jobs) + 1,'{0}','{1}','{2}','{3}')".format(bId,number,price ,text)
      query.exec_(sql)
      query.exec_('select hours, price,job,id from jobs order by id desc limit 1')
      return self.extractJobs(query)[0]

# kanske en nivå för varningar?
   def validateForSubmit(self):
      errorMsgs = []
      reference = self.ui.referenceField.text()
      if reference == "":
         errorMsgs.append("Du har glömt referensfältet")
      counter = 1
      for j in self.jobList:

         if j.ui.description.text() == "":
            errorMsgs.append("Du har glömt beskrivning på job " + str(counter))
         try:
            int( j.ui.price.text())
         except Exception:
            errorMsgs.append("Det ser inte ut som en siffra på priset på job " + str(counter))
         try:
            int( j.ui.number.text())
         except Exception:
            errorMsgs.append("Det ser inte ut som en siffra på antalet på job " + str(counter))
         counter += 1
      #TODO: if new customer is added
      if self.newCustomerActivated:
         if self.newCustomerForm.ui.name.text() == "":
            errorMsgs.append("Det finns inget namn på den nya kunden")
         if self.newCustomerForm.ui.address.text() == "":
            errorMsgs.append("Det finns ingen address på den nya kunden")
         if self.newCustomerForm.ui.zip.text() == "":
            errorMsgs.append("Det finns inget postnummer på den nya kunden")

      if len(errorMsgs) != 0:
         errWidget = QErrorMessage(self)
         errWidget.showMessage("<br/>".join(errorMsgs))
         return False
      return True
         
            
            

   @pyqtSlot()
   def on_saveGenerateButton_clicked(self):
      if not self.validateForSubmit():
         return
      query = QSqlQuery()
      dateFormat = 'yyyy-MM-dd'
      date = QDate.currentDate()
      customer = None
      if self.newCustomerActivated:
         name = self.newCustomerForm.ui.name.text()
         address = self.newCustomerForm.ui.address.text()
         zip = self.newCustomerForm.ui.zip.text()
         customer = self.newCustomer(name, address, zip)
      else:
         customerId = self.ui.customerChooser.currentIndex() + 1
         query.exec_('select id, name,address, zipcode from customer where id=' + str(customerId))
         query.next()
         customer = self.extractCustomer(query)

      customerId = customer.id
      bill = self.newBill(self.ui.referenceField.text(),customerId)
      bill.setCustomer(customer)
      for j in self.jobList:
         text = j.ui.description.text()
         price = int( j.ui.price.text())
         number = int( j.ui.number.text())
         job = self.newJob(price,number, text, bill.id)
         bill.addJob(job)

      #kodduplikat, lägg ut i fun
      pdf = pdflib.BillGenerator(bill)
      if pdf.fileExsists:
         print("file exists")
      else:
         print("file does NOT exist")

      fileName = pdf.generate()
      webbrowser.open(fileName) 
      

      
      
   
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

      fileName = pdf.generate()
      webbrowser.open(fileName) 
      


   @pyqtSlot()
   def on_newCustomerButton_clicked(self):
##TODO: det ska gå att ta bort newcustmerform
      if self.newCustomerActivated == True:
         self.newCustomerActivated = False
         self.newCustomerForm.hide()
         self.ui.newCustomerButton.setText("Ny")
      else:
         self.newCustomerActivated = True
         self.newCustomerForm.show()
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
