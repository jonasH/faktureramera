#!/usr/bin/env python3
from PySide2.QtWidgets import QMessageBox
from PySide2.QtSql import QSqlQuery, QSqlDatabase

import os


def openDatabase(database_name='fmdb.sqlite'):
    db = QSqlDatabase.addDatabase('QSQLITE')
    # TODO: make this a variable in the profile
    init_db = not os.path.exists(database_name)
    db.setDatabaseName(database_name)
    if not db.open():
        QMessageBox.critical(None,
                             f"OMG ERROR! withz the database: {database_name}",
                             QMessageBox.Cancel)
        return False
    query = QSqlQuery()
    if init_db:
        with open(os.path.join(os.getcwd(), "misc/fm.sql")) as f:
            for i in f:
                query.exec_(i)

    return True
