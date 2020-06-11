from PySide2.QtWidgets import QApplication
from ext.pyside2_sqlite_db import PySide2SqliteDb
from ext.pdf_generator import generate_pdf
from ext.config_parser_settings import ConfigParserSettings
from domain.app import FM
from ui.faktureramerawindow import FaktureraMeraWindow
import sys
from support import settings_folder
import os
from PySide2.QtCore import QTranslator


def main():
    app = QApplication(sys.argv)
    translator = QTranslator()
    user_settings_folder = settings_folder()
    if not os.path.exists(user_settings_folder):
        os.mkdir(user_settings_folder)
    db_path = os.path.join(user_settings_folder, "fm.sqlite")
    db = PySide2SqliteDb(db_path)
    settings = ConfigParserSettings(user_settings_folder)
    with FM(db, generate_pdf, settings) as fm:
        faktureramera = FaktureraMeraWindow(fm, translator)
        faktureramera.show()
        exit_val = app.exec_()
    sys.exit(exit_val)


if __name__ == "__main__":
    main()
