import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

## TODO: move this to a "model" module
# TODO: generate getters/setters
class Job():
    price = 0
    number = 0
    text = ""
    def __init__(self, price, number,text ):
        self.price = price
        self.number = number
        self.text = text

class Customer():
    id

# TODO: generate getters/setters
class Bill():
    date = ""
    idNr = 0
    ref = ""
    name = ""
    address = ""
    zipCode = ""
    jobs = []

    def __init__(self, idNr, date, ref, name, address, zipCode):
         self.date, self.idNr, self.ref, self.name, self.address, self.zipCode = date, idNr, ref, name, address, zipCode

    
    def addJob(self,job):
        self.jobs.append(job)

    def removeJob(self, job):
        self.jobs.remove(job)
    

class BillGenerator():
    """A class that will generate a bill"""
    headingFont  = QFont("Times", 22)
    normalFont = QFont("Times", 12)
    fineFont = QFont("Times", 8)
    doc = QPdfWriter("test.pdf")
    painter = QPainter()
    normalRowDistance = 250

    #def __init__(self):

        
    
    def generate(self):
        """Print a new bill"""
        self.painter.begin(self.doc)
        self.printHeading()
        self.printInformation()
        self.printSpecificationTemplate()
        self.painter.end()

    def printHeading(self):
        """Helper function for printing the header of the bill"""
        self.painter.setFont(self.headingFont)
        self.painter.drawText(self.doc.width() / 2 - 800,self.doc.height() / 14,"FAKTURA")

    def printInformation(self):
        """Print two columns with information about the bill"""
        xFirst = self.doc.width() / 10
        yFirst = self.doc.height() / 10
        xSecond = self.doc.width() / 2 + self.doc.width() / 10
        
        self.painter.setFont(self.normalFont)
        
        # first column
        self.painter.drawText(xFirst, yFirst, "Datum: ")
        self.painter.drawText(xFirst, yFirst + self.normalRowDistance, "Fakturanummer: ")
        self.painter.drawText(xFirst, yFirst + self.normalRowDistance * 2, "Förfallodag: ")
        self.painter.drawText(xFirst, yFirst + self.normalRowDistance * 3, "Er Referens: ")


        # second column
        # TODO: take care of long names
        self.painter.drawText(xSecond, yFirst, "?? mottagare ??")
        self.painter.drawText(xSecond, yFirst + self.normalRowDistance, "??adress??")
        self.painter.drawText(xSecond, yFirst + self.normalRowDistance * 2, "??postnr + ort?? ")
        
        
    def printSpecificationTemplate(self):
        """Draw the specification of the bill"""
        # TODO: move this to a membervar(xFirst)
        # TODO: maybe shorten this function?
        margin = self.doc.width() / 10
        yFirstLine = self.doc.height() / 3
        yThirdLine = (self.doc.height() / 4) * 3
        pen = QPen()
        pen.setWidth(10)

        # draw lines
        self.painter.setPen(pen)
        self.painter.drawLine(margin, yFirstLine , self.doc.width() - margin, yFirstLine)
        self.painter.drawLine(margin, yFirstLine + self.normalRowDistance * 2 , self.doc.width() - margin, yFirstLine + self.normalRowDistance * 2 )
        self.painter.drawLine(margin, yThirdLine , self.doc.width() - margin, yThirdLine )
        self.painter.drawLine(self.doc.width() - margin * 3, yThirdLine + self.normalRowDistance * 3 , self.doc.width() - margin, yThirdLine + self.normalRowDistance * 3)
        self.painter.drawLine(margin, yThirdLine + self.normalRowDistance * 5 , self.doc.width() - margin, yThirdLine + self.normalRowDistance * 5)
        # text section
        self.painter.setFont(self.normalFont)
        self.painter.drawText(margin, yFirstLine + self.normalRowDistance , " Specification")
        self.painter.drawText(margin * 6, yFirstLine + self.normalRowDistance , " Antal")
        self.painter.drawText(margin * 7, yFirstLine + self.normalRowDistance , " a kronor")
        self.painter.drawText(margin * 8, yFirstLine + self.normalRowDistance , " Totalt")
        
        self.painter.drawText(margin * 8, yThirdLine +self.normalRowDistance , "Summa: ")
        self.painter.drawText(margin * 8, yThirdLine +self.normalRowDistance*2 , "Moms: ")
        self.painter.drawText(margin * 8, yThirdLine +self.normalRowDistance*4 , "Totalt: ")

        self.painter.setFont(self.fineFont)
        self.painter.drawText(margin, yThirdLine +self.normalRowDistance*6 , "Adress: ")
        self.painter.drawText(margin*4, yThirdLine +self.normalRowDistance*6 , "Telefon: ")
        self.painter.drawText(margin*6, yThirdLine +self.normalRowDistance*6 , "Mail: ")
        self.painter.drawText(margin*8, yThirdLine +self.normalRowDistance*6 , "Momsreg.nr/org.nr: ")
        self.painter.drawText(margin*8, yThirdLine +self.normalRowDistance*7 , "Bankgiro ")
        self.painter.drawText(margin*8, yThirdLine +self.normalRowDistance*8 , "Företaget innehar F-skattebevis ")

        

