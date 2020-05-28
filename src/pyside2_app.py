from PySide2.QtWidgets import QApplication
from ext.pyside2_sqlite_db import PySide2SqliteDb
from ext.pdf_generator import generate_pdf
from domain.app import FM
from ui.faktureramerawindow import FaktureraMeraWindow
import sys
from support import settings_folder
import os


def main():
    app = QApplication(sys.argv)
    user_settings_folder = settings_folder()
    if not os.path.exists(user_settings_folder):
        os.mkdir(user_settings_folder)
    db_path = os.path.join(user_settings_folder, "fm.sqlite")
    db = PySide2SqliteDb(db_path)
    fm = FM(db, generate_pdf)
    faktureramera = FaktureraMeraWindow(fm)

    faktureramera.ui.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
