#!/usr/bin/env python3
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtSql import (QSqlQuery, QSqlDatabase)

import os


def openDatabase(databaseName='fmdb.sqlite'):
    db = QSqlDatabase.addDatabase('QSQLITE') 
    #TODO: make this a variable in the profile
    dbPath = os.getcwd() + '/fm.sqlite'
    

    db.setDatabaseName(dbPath)
    if not db.open():
         QMessageBox.critical(None," OMG ERROR! withz the database: " + databaseName,
                QMessageBox.Cancel)
         return False
    query = QSqlQuery()
 #   if not os.path.exists(dbPath):
    for i in open("/home/jonas/Kod/FaktureraMera2/misc/fakturabackup.sqlite"):
        query.exec_(i)
        print(query.lastError().text())
   
    result = query.exec_('select * from bill')
    print(result)
    return True

