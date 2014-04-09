#!/usr/bin/env python3
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtSql import (QSqlQuery, QSqlDatabase)


def openDatabase(databaseName='fmdb.sqlite'):
    db = QSqlDatabase.addDatabase('QSQLITE') 
#TODO: make this a variable
    db.setDatabaseName(':memory:')
    if not db.open():
         QMessageBox.critical(None," OMG ERROR! withz the database: " + databaseName,
                QMessageBox.Cancel)
         return False
    query = QSqlQuery()
    for i in open("/home/jonas/Kod/FaktureraMera2/misc/fakturabackup.sqlite"):
        query.exec_(i)
        print(query.lastError().text())
   
    result = query.exec_('select * from bill')
    print(result)
    return True

