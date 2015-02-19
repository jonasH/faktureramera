import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


try:
    import fakturamodel
except Exception:
    import lib.fakturamodel as fakturamodel

from math import floor, ceil

# TODO: variablealize bunch of selfies
class BillGenerator():
    """A class that will generate a bill"""
    headingFont = QFont("Times", 22)
    normalFont = QFont("Times", 12)
    fineFont = QFont("Times", 8)
    companyFont = QFont("Times", 18)

    painter = QPainter()
    normalRowDistance = 250

    def __init__(self, bill):
        self.bill = bill
        self.profile = fakturamodel.Profile()
        if not os.path.exists(self.profile.billLocation):
            os.mkdir(self.profile.billLocation)
        print(bill.id)
        self.fileName = self.profile.billLocation + str(bill.id) + "-" + bill.customer.name + ".pdf"
        self.doc = QPdfWriter(self.fileName)
        self.fileExsists = os.path.exists(self.fileName)

        self.margin = self.doc.width() / 10

    def generate(self):
        """Print a new bill"""
        # TODO: check if file exists!
        self.painter.begin(self.doc)
        self.printCompanyName()
        self.printHeading()
        self.printInformation()
        self.printSpecificationTemplate()
        self.printSpecification()
        self.painter.end()
        return self.fileName

    def printCompanyName(self):
        self.painter.setFont(self.companyFont)
        for i, txt in enumerate(self.profile.companyName):
            self.painter.drawText(50, i * 350 + 200, txt)

    def printHeading(self):
        """Helper function for printing the header of the bill"""
        self.painter.setFont(self.headingFont)
        self.painter.drawText(self.doc.width() / 2 - 800, self.doc.height() / 14, "FAKTURA")

    def printInformation(self):
        """Print two columns with information about the bill"""
        xFirst = self.doc.width() / 10
        yFirst = self.doc.height() / 10
        xSecond = self.doc.width() / 2 + self.doc.width() / 10
        y, m, d = self.bill.bill_date.split('-')
        date = QDate(int(y), int(m), int(d))
        dateFormat = 'yyyy-MM-dd'
        ##  TODO: make this number changable in the profile
        payDay = date.addDays(self.profile.daysToPay)

        self.painter.setFont(self.normalFont)

        # first column
        self.painter.drawText(xFirst, yFirst, "Datum: " + date.toString(dateFormat))
        self.painter.drawText(xFirst, yFirst + self.normalRowDistance, "Fakturanummer: " + str(self.bill.id))
        self.painter.drawText(xFirst, yFirst + self.normalRowDistance * 2,
                              "Förfallodag: " + payDay.toString(dateFormat))
        self.painter.drawText(xFirst, yFirst + self.normalRowDistance * 3, "Er Referens: " + self.bill.reference)


        # second column

        if len(self.bill.customer.name) > 25:
            split = self.bill.customer.name.rsplit(' ')
            self.painter.drawText(xSecond, yFirst, " ".join(split[0:floor(len(split) / 2)]))
            self.painter.drawText(xSecond, yFirst + self.normalRowDistance, " ".join(split[ceil(len(split) / 2):]))
            self.painter.drawText(xSecond, yFirst + self.normalRowDistance * 2, self.bill.customer.address)
            self.painter.drawText(xSecond, yFirst + self.normalRowDistance * 3, self.bill.customer.zipcode)
        else:
            self.painter.drawText(xSecond, yFirst, self.bill.customer.name)
            self.painter.drawText(xSecond, yFirst + self.normalRowDistance, self.bill.customer.address)
            self.painter.drawText(xSecond, yFirst + self.normalRowDistance * 2, self.bill.customer.zipcode)


    def printSpecificationTemplate(self):
        """Draw the specification of the bill"""
        # TODO: maybe shorten this function?
        # TODO: globlaize column sync with below
        yFirstLine = self.doc.height() / 3
        yThirdLine = (self.doc.height() / 4) * 3
        pen = QPen()
        pen.setWidth(10)

        # draw lines
        self.painter.setPen(pen)
        self.painter.drawLine(self.margin, yFirstLine, self.doc.width() - self.margin, yFirstLine)
        self.painter.drawLine(self.margin, yFirstLine + self.normalRowDistance * 2,
                              self.doc.width() - self.margin, yFirstLine + self.normalRowDistance * 2)
        self.painter.drawLine(self.margin, yThirdLine, self.doc.width() - self.margin, yThirdLine)
        self.painter.drawLine(self.doc.width() - self.margin * 3, yThirdLine + self.normalRowDistance * 3,
                              self.doc.width() - self.margin, yThirdLine + self.normalRowDistance * 3)
        self.painter.drawLine(self.margin, yThirdLine + self.normalRowDistance * 5,
                              self.doc.width() - self.margin, yThirdLine + self.normalRowDistance * 5)
        # text section
        self.painter.setFont(self.normalFont)
        self.painter.drawText(self.margin, yFirstLine + self.normalRowDistance, " Specification")
        self.painter.drawText(self.margin * 6, yFirstLine + self.normalRowDistance, " Antal")
        self.painter.drawText(self.margin * 7, yFirstLine + self.normalRowDistance, " a kronor")
        self.painter.drawText(self.margin * 8, yFirstLine + self.normalRowDistance, " Totalt")

        self.painter.drawText(self.margin * 7, yThirdLine + self.normalRowDistance, "Summa: ")
        self.painter.drawText(self.margin * 7, yThirdLine + self.normalRowDistance * 2, "Moms: ")
        self.painter.drawText(self.margin * 7, yThirdLine + self.normalRowDistance * 4, "Totalt: ")

        self.painter.setFont(self.fineFont)
        self.painter.drawText(self.margin, yThirdLine + self.normalRowDistance * 6,
                              "Adress: " + self.profile.address)
        self.painter.drawText(self.margin * 4, yThirdLine + self.normalRowDistance * 6,
                              "Telefon: " + self.profile.telephone)
        self.painter.drawText(self.margin * 6, yThirdLine + self.normalRowDistance * 6,
                              "Mail: " + self.profile.mail)
        self.painter.drawText(self.margin * 8, yThirdLine + self.normalRowDistance * 6,
                              "Momsreg.nr/org.nr: " + self.profile.orgNr)
        self.painter.drawText(self.margin * 8, yThirdLine + self.normalRowDistance * 7,
                              "Bankgiro " + self.profile.bankAccount)
        self.painter.drawText(self.margin * 8, yThirdLine + self.normalRowDistance * 8,
                              "Företaget innehar F-skattebevis ")


    def printSpecification(self):
        """"""
        # TODO:  globlaize column sync with above
        yFirstLine = self.doc.height() / 3 + (self.normalRowDistance * 3)
        yThirdLine = (self.doc.height() / 4) * 3
        secondCol = self.margin * 6
        thirdCol = self.margin * 7
        fourthCol = self.margin * 8
        self.painter.setFont(self.normalFont)

        i = 0
        totalSum = 0
        for job in self.bill.jobs:
            yLine = yFirstLine + self.normalRowDistance * i
            self.painter.drawText(self.margin, yLine, job.text)
            self.painter.drawText(secondCol, yLine, str(job.number))
            self.painter.drawText(thirdCol, yLine, "{:10.2f}".format(job.price))
            self.painter.drawText(fourthCol, yLine, "{:10.2f}".format(job.price * job.number))
            totalSum += job.price * job.number
            i += 1

        self.painter.drawText(fourthCol, yThirdLine + self.normalRowDistance, "{:10.2f}".format(totalSum))
        tax = totalSum * self.profile.tax
        self.painter.drawText(fourthCol, yThirdLine + self.normalRowDistance * 2, "{:10.2f}".format(tax))
        self.painter.drawText(fourthCol, yThirdLine + self.normalRowDistance * 4, "{:10.2f}".format(totalSum + tax))
