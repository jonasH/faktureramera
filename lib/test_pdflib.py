#!/usr/bin/env python3
import sys
import pdflib
from PyQt5.QtWidgets import *

app = QApplication(sys.argv)
pdf = pdflib.BillGenerator()
pdf.generate()
