from PySide2.QtWidgets import QApplication
from ext.pyside2_sqlite_db import PySide2SqliteDb
from ext.pdf_generator import generate_pdf
from domain.app import FM
from ui.faktureramerawindow import FaktureraMeraWindow
import sys


def main():

    app = QApplication(sys.argv)
    db = PySide2SqliteDb("fm.sqlite")
    fm = FM(db, generate_pdf)
    faktureramera = FaktureraMeraWindow(fm)

    faktureramera.ui.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
