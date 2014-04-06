#!/usr/bin/env python3
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtSql import (QSqlQuery, QSqlDatabase)


def openDatabase(databaseName='fmdb.sqlite'):
    db = QSqlDatabase.addDatabase('QSQLITE') 
    db.setDatabaseName(databaseName)
    if not db.open():
         QMessageBox.critical(None," OMG ERROR! withz the database: " + databaseName,
                QMessageBox.Cancel)
         return False
    return db


    

if __name__ == '__main__':
    import sys
    
    app = QApplication(sys.argv)
    if not openDatabase() :
        sys.exit(1)

    query = QSqlQuery()
    query.exec_("create table employee(id int, name varchar(20), city int, country int)")
    query.exec_("insert into employee values(1, 'Espen', 5000, 47)")

    sys.exit(app.exec_())
