#!/usr/bin/env python3
import sys
import pdflib
from PyQt5.QtWidgets import *
import fakturamodel

app = QApplication(sys.argv)

job = fakturamodel.Job(100,3,"Jobbat i skog")
job1 = fakturamodel.Job(140,2,"Jobbat med plantor")
job2 = fakturamodel.Job(300,5,"Kört lite bil")
customer = fakturamodel.Customer(1,"Jonas Berg", "Apgatan10", "1010 Stockholm")
bill = fakturamodel.Bill(1,"Mr Berg", "2014-04-04")
bill.setCustomer(customer)
bill.addJob(job)
bill.addJob(job1)
bill.addJob(job2)
pdf = pdflib.BillGenerator(bill)
pdf.generate()
