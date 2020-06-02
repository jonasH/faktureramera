from PySide2.QtWidgets import QApplication
from ext.pyside2_sqlite_db import PySide2SqliteDb

# from ext.pdf_generator import generate_pdf
from domain.app import FM
from ui.faktureramerawindow import FaktureraMeraWindow
import os
from unittest.mock import patch
from ext.config_parser_settings import ConfigParserSettings
from ext.pdf_generator import generate_pdf
import pytest
import shutil


def __create_first_customer_and_bill(faktureramera, open_file, exp_report_path):
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
    open_file.assert_called_once_with(exp_report_path)
    open_file.reset_mock()


def __regenerate_bill(faktureramera, open_file, exp_report_path):
    faktureramera.ui.tableView.selectRow(0)
    faktureramera.on_generateButton_clicked()
    open_file.assert_called_once_with(exp_report_path)
    open_file.reset_mock()


def __change_bill(faktureramera, open_file, exp_report_path):
    faktureramera.ui.tableView.selectRow(0)
    faktureramera.on_editBillButton_clicked()
    faktureramera.on_addJobButton_clicked()
    assert len(faktureramera.jobList) == 2
    job_form = faktureramera.jobList[1]

    job_form.description.setText("aqqqsfd")
    job_form.price.setText("305")
    job_form.number.setText("42")
    faktureramera.on_saveGenerateButton_clicked()
    open_file.assert_called_once_with(exp_report_path)
    open_file.reset_mock()


def __maculate_bill(faktureramera):
    assert faktureramera.ui.tableView.model().rowCount() == 1
    faktureramera.ui.tableView.selectRow(0)
    faktureramera.on_maculateButton_clicked()
    assert faktureramera.ui.tableView.model().rowCount() == 0


@pytest.fixture
def user_settings_folder():
    directory = os.path.dirname(__file__)
    user_settings_folder = os.path.join(directory, "..", "..", "build", "e2e__settings")
    shutil.rmtree(user_settings_folder, ignore_errors=True)
    os.makedirs(user_settings_folder)
    return user_settings_folder


@pytest.fixture(scope="module")
def qapp():
    return QApplication([])


@pytest.mark.usefixtures("qapp")
@patch("ui.faktureramerawindow.open_file")
def test_bills(open_file, user_settings_folder):
    test_db_name = os.path.join(user_settings_folder, "e2e.sqlite")
    db = PySide2SqliteDb(test_db_name)
    exp_report_path = os.path.join(user_settings_folder, "Bills", "1-asfd.pdf")
    settings = ConfigParserSettings(user_settings_folder)
    # intentionally not using with-statement to not save settings
    fm = FM(db, generate_pdf, settings)
    faktureramera = FaktureraMeraWindow(fm)
    __create_first_customer_and_bill(faktureramera, open_file, exp_report_path)
    __regenerate_bill(faktureramera, open_file, exp_report_path)
    __change_bill(faktureramera, open_file, exp_report_path)
    __maculate_bill(faktureramera)


def __confirm_old_settings_in_gui(faktureramera, old_profile):
    assert old_profile.days_to_pay == int(faktureramera.ui.due_date_input.value())
    assert old_profile.address == faktureramera.ui.address_input.text()
    assert old_profile.mail == faktureramera.ui.mail_input.text()
    assert old_profile.telephone == faktureramera.ui.telephone_input.text()
    assert old_profile.org_nr == faktureramera.ui.org_nr_input.text()
    assert old_profile.bank_account == faktureramera.ui.bank_no_input.text()
    assert old_profile.tax == float(faktureramera.ui.tax_input.value() / 100.0)
    assert old_profile.company_name == faktureramera.ui.company_name_input.text()


@pytest.mark.usefixtures("qapp")
def test_user_settings(user_settings_folder):
    test_db_name = os.path.join(user_settings_folder, "e2e.sqlite")
    db = PySide2SqliteDb(test_db_name)
    settings = ConfigParserSettings(user_settings_folder)
    exp_due_date = 35
    exp_address = "havcabtta"
    exp_mail = "havcabtta2"
    exp_tele = "havcabtta3"
    exp_org = "havcabtta45"
    exp_bank = "havcabtta52"
    exp_tax = 0.23
    exp_name = "havcabtta34"
    # Make sure the we're changing stuff
    old_profile = settings.profile()
    assert old_profile.days_to_pay != exp_due_date
    assert old_profile.address != exp_address
    assert old_profile.mail != exp_mail
    assert old_profile.telephone != exp_tele
    assert old_profile.org_nr != exp_org
    assert old_profile.bank_account != exp_bank
    assert old_profile.tax != exp_tax
    assert old_profile.company_name != exp_name

    with FM(db, generate_pdf, settings) as fm:
        faktureramera = FaktureraMeraWindow(fm)
        __confirm_old_settings_in_gui(faktureramera, old_profile)
        faktureramera.ui.due_date_input.setValue(exp_due_date)
        faktureramera.ui.address_input.setText(exp_address)
        faktureramera.ui.mail_input.setText(exp_mail)
        faktureramera.ui.telephone_input.setText(exp_tele)
        faktureramera.ui.org_nr_input.setText(exp_org)
        faktureramera.ui.bank_no_input.setText(exp_bank)
        faktureramera.ui.tax_input.setValue(exp_tax * 100)
        faktureramera.ui.company_name_input.setText(exp_name)
        faktureramera.on_save_profile()

    settings = ConfigParserSettings(user_settings_folder)
    new_profile = settings.profile()
    assert new_profile.days_to_pay == exp_due_date
    assert new_profile.address == exp_address
    assert new_profile.mail == exp_mail
    assert new_profile.telephone == exp_tele
    assert new_profile.org_nr == exp_org
    assert new_profile.bank_account == exp_bank
    assert new_profile.tax == exp_tax
    assert new_profile.company_name == exp_name
