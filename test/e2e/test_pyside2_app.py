from PySide2.QtWidgets import QApplication
from ext.pyside2_sqlite_db import PySide2SqliteDb

# from ext.pdf_generator import generate_pdf
from domain.app import FM
from ui.faktureramerawindow import FaktureraMeraWindow
import os
from unittest.mock import Mock, patch
from ext.config_parser_settings import ConfigParserSettings
from ext.pdf_generator import generate_pdf


def __create_first_customer_and_bill(faktureramera, webbrowser, exp_report_path):
    faktureramera.on_newCustomerButton_clicked()
    faktureramera.newCustomerForm.name.setText("asfd")
    faktureramera.newCustomerForm.address.setText("300")
    faktureramera.newCustomerForm.zip.setText("40")

    faktureramera.ui.referenceField.setText("Viktor")

    job_form = faktureramera.jobList[0]

    job_form.description.setText("asfd")
    job_form.price.setText("300")
    job_form.number.setText("40")

    # Add job, remove job
    faktureramera.on_addJobButton_clicked()
    assert len(faktureramera.jobList) == 2
    faktureramera.on_removeJobButton_clicked()
    assert len(faktureramera.jobList) == 1
    faktureramera.on_removeJobButton_clicked()
    assert len(faktureramera.jobList) == 1
    faktureramera.on_saveGenerateButton_clicked()
    webbrowser.open.assert_called_once_with(exp_report_path)
    webbrowser.open.reset_mock()


def __regenerate_bill(faktureramera, webbrowser, exp_report_path):
    faktureramera.ui.tableView.selectRow(0)
    faktureramera.on_generateButton_clicked()
    webbrowser.open.assert_called_once_with(exp_report_path)
    webbrowser.open.reset_mock()


def __change_bill(faktureramera, webbrowser, exp_report_path):
    faktureramera.ui.tableView.selectRow(0)
    faktureramera.on_editBillButton_clicked()
    faktureramera.on_addJobButton_clicked()
    assert len(faktureramera.jobList) == 2
    job_form = faktureramera.jobList[1]

    job_form.description.setText("aqqqsfd")
    job_form.price.setText("305")
    job_form.number.setText("42")
    faktureramera.on_saveGenerateButton_clicked()
    webbrowser.open.assert_called_once_with(exp_report_path)
    webbrowser.open.reset_mock()


def __maculate_bill(faktureramera):
    assert faktureramera.ui.tableView.model().rowCount() == 1
    faktureramera.ui.tableView.selectRow(0)
    faktureramera.on_maculateButton_clicked()
    assert faktureramera.ui.tableView.model().rowCount() == 0


@patch("ui.faktureramerawindow.webbrowser")
def test_long_name(webbrowser):
    QApplication([])
    test_db_name = "e2e.sqlite"
    if os.path.exists(test_db_name):
        os.unlink(test_db_name)
    db = PySide2SqliteDb(test_db_name)
    directory = os.path.dirname(__file__)
    user_settings_folder = os.path.join(directory, "..", "..", "build", "test_settings")
    exp_report_path = os.path.join(user_settings_folder, "Bills", '1-asfd.pdf')
    settings = ConfigParserSettings(user_settings_folder)
    fm = FM(db, generate_pdf, settings)
    faktureramera = FaktureraMeraWindow(fm)
    __create_first_customer_and_bill(faktureramera, webbrowser, exp_report_path)
    __regenerate_bill(faktureramera, webbrowser, exp_report_path)
    __change_bill(faktureramera, webbrowser, exp_report_path)
    __maculate_bill(faktureramera)
