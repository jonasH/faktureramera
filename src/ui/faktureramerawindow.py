from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QErrorMessage,
    QPushButton,
)
from PySide2.QtSql import QSqlQueryModel
from PySide2.QtCore import Qt, QFile, QObject, QEvent
from PySide2.QtUiTools import QUiLoader
import os
from domain.model import Job, Profile
from support import resource_path
import platform
from typing import List
import subprocess


def load_ui(filename):
    module_dir = os.path.dirname(__file__)
    module_dir = resource_path(module_dir)
    file_name = os.path.join(module_dir, filename)
    qfile = QFile(file_name)
    qfile.open(QFile.ReadOnly)
    loader = QUiLoader()
    return loader.load(qfile)


def open_file(filepath):
    if platform.system() == "Windows":  # Windows
        os.startfile(filepath)
    else:
        subprocess.call(("xdg-open", filepath))


class NewJobFilter(QObject):
    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.parent().add_job_widget()
            return True
        else:
            # standard event processing
            return QObject.eventFilter(self, obj, event)


class FaktureraMeraWindow(QMainWindow):
    def __init__(self, app, parent=None, load_data=True):
        """"""
        super(FaktureraMeraWindow, self).__init__(parent)
        self.app = app
        self.edit_bill_id = 0
        self.tab_new_job_filter = NewJobFilter(self)
        self.jobList = []
        self.setup_ui()
        if load_data:
            self.load_data()

    def load_data(self):
        self.updateHistoryTable()
        self.populateCustomers()
        self.load_settings_data()

    def load_settings_data(self):
        profile = self.app.profile()
        self.ui.due_date_input.setValue(profile.days_to_pay)
        self.ui.address_input.setText(profile.address)
        self.ui.mail_input.setText(profile.mail)
        self.ui.telephone_input.setText(profile.telephone)
        self.ui.org_nr_input.setText(profile.org_nr)
        self.ui.bank_no_input.setText(profile.bank_account)
        self.ui.tax_input.setValue(profile.tax * 100)
        self.ui.company_name_input.setText(profile.company_name)

    def setup_ui(self) -> None:
        self.ui = load_ui("faktureramera.ui")
        btn = self.ui.findChild(QPushButton, "newCustomerButton")
        btn.clicked.connect(self.on_newCustomerButton_clicked)
        btn = self.ui.findChild(QPushButton, "saveGenerateButton")
        btn.clicked.connect(self.on_saveGenerateButton_clicked)
        btn = self.ui.findChild(QPushButton, "zeroButton")
        btn.clicked.connect(self.on_zeroButton_clicked)
        btn = self.ui.findChild(QPushButton, "editBillButton")
        btn.clicked.connect(self.on_editBillButton_clicked)
        btn = self.ui.findChild(QPushButton, "addJobButton")
        btn.clicked.connect(self.on_addJobButton_clicked)
        btn = self.ui.findChild(QPushButton, "removeJobButton")
        btn.clicked.connect(self.on_removeJobButton_clicked)
        btn = self.ui.findChild(QPushButton, "maculateButton")
        btn.clicked.connect(self.on_maculateButton_clicked)
        btn = self.ui.findChild(QPushButton, "generateButton")
        btn.clicked.connect(self.on_generateButton_clicked)
        btn = self.ui.findChild(QPushButton, "open_bills_btn")
        btn.clicked.connect(self.on_open_bills)
        btn = self.ui.findChild(QPushButton, "save_profile_btn")
        btn.clicked.connect(self.on_save_profile)
        self.newCustomerForm = load_ui("newcustomerform.ui")
        self.newCustomerForm.hide()
        self.ui.newCustomerLayout.addWidget(self.newCustomerForm)
        self.add_job_widget()

    def on_open_bills(self):
        open_file(self.app.bills_location)

    def on_save_profile(self):
        days_to_pay = self.ui.due_date_input.value()
        address = self.ui.address_input.text()
        mail = self.ui.mail_input.text()
        tele = self.ui.telephone_input.text()
        org_nr = self.ui.org_nr_input.text()
        bank_account = self.ui.bank_no_input.text()
        tax = self.ui.tax_input.value() / 100.0
        name = self.ui.company_name_input.text()
        p = Profile(days_to_pay, address, mail, tele, org_nr, bank_account, tax, name)
        self.app.save_profile(p)

    def populateCustomers(self) -> None:
        self.ui.customerChooser.clear()
        for c in self.app.fetch_customers():
            self.ui.customerChooser.addItem(c.name)

    def __validate_job(self, j, counter: int) -> List[str]:
        error_msgs = []
        if j.description.text() == "":
            error_msgs.append(f"Description is empty for job {counter}")
        if j.price.value() == 0.0:
            error_msgs.append(f"Price is zero for job {counter}")
        if j.number.value() == 0:
            error_msgs.append(f"Number is zero for job {counter}")
        return error_msgs

    def __validate_new_customer(self) -> List[str]:
        err_msgs = []
        if self.newCustomerForm.name.text() == "":
            err_msgs.append("Det finns inget namn pa den nya kunden")
        if self.newCustomerForm.address.text() == "":
            err_msgs.append("Det finns ingen address pa den nya kunden")
        if self.newCustomerForm.zip.text() == "":
            err_msgs.append("Det finns inget postnummer pa den nya kunden")
        return err_msgs

    def validate_for_submit(self):
        error_msgs = []
        reference = self.ui.referenceField.text()
        if reference == "":
            error_msgs.append("You have forgotten the reference field")

        for counter, j in enumerate(self.jobList, 1):
            error_msgs += self.__validate_job(j, counter)
        if self.newCustomerActivated:
            error_msgs += self.__validate_new_customer()
        if len(error_msgs) != 0:
            errWidget = QErrorMessage(self)
            errWidget.showMessage("<br/>".join(error_msgs))
            return False
        return True

    def on_zeroButton_clicked(self):
        self.reinitUI()

    def on_editBillButton_clicked(self):
        self.ui.tabWidget.setCurrentIndex(0)
        self.reinitUI()
        billId = self.__getBillidFromHistory()
        if billId == -1:
            return
        bill = self.app.fetch_bill(billId)
        self.poulateBillData(bill)
        self.edit_bill_id = billId
        self.ui.saveGenerateButton.setText("Uppdatera")

    def poulateBillData(self, bill):
        """"""
        self.ui.customerChooser.setCurrentIndex(bill.customer.id - 1)
        self.ui.referenceField.setText(bill.reference)
        for j in bill.jobs:
            if self.jobList[-1].description.text() != "":
                self.add_job_widget()
            job = self.jobList[-1]
            job.description.setText(j.text)
            job.number.setValue(j.number)
            job.price.setValue(j.price)

    def reinitUI(self):
        self.edit_bill_id = 0
        self.ui.saveGenerateButton.setText("Generera")
        numberOfJobs = len(self.jobList)
        for i in range(numberOfJobs):
            self.removeJobWidget()
        self.add_job_widget()
        self.ui.referenceField.clear()
        self.hideNewCustomer()

    def __current_customer(self):
        if self.newCustomerActivated:
            name = self.newCustomerForm.name.text()
            address = self.newCustomerForm.address.text()
            zip_code = self.newCustomerForm.zip.text()
            customer = self.app.create_customer(name, address, zip_code)
        else:
            customer_id = self.ui.customerChooser.currentIndex() + 1
            customer = self.app.fetch_customer(customer_id)
        return customer

    def on_saveGenerateButton_clicked(self):
        if not self.validate_for_submit():
            return

        customer = self.__current_customer()
        customer_id = customer.id
        reference = self.ui.referenceField.text()
        jobs = []
        for j in self.jobList:
            text = j.description.text()
            price = j.price.value()
            number = j.number.value()
            jobs.append(Job(price, number, text))

        if self.edit_bill_id == 0:
            bill = self.app.create_bill(reference, customer_id, jobs)

        else:
            bill = self.app.update_bill(self.edit_bill_id, reference, customer_id, jobs)

        fileName = self.app.generate_bill(bill)
        self.reinitUI()
        self.updateHistoryTable()
        self.populateCustomers()
        open_file(fileName)

    def removeJobWidget(self):
        job = self.jobList[-1]
        job.hide()
        self.ui.jobsLayout.removeWidget(job)
        QApplication.processEvents()
        self.jobList.remove(job)

    def add_job_widget(self,):
        if len(self.jobList) > 0:
            self.jobList[-1].number.removeEventFilter(self.tab_new_job_filter)
        job = load_ui("jobform.ui")
        self.ui.jobsLayout.addWidget(job)
        self.jobList.append(job)
        job.number.installEventFilter(self.tab_new_job_filter)

    def on_addJobButton_clicked(self):
        self.add_job_widget()
        QApplication.processEvents()

    def on_removeJobButton_clicked(self):
        if len(self.jobList) == 1:
            return
        self.removeJobWidget()

    def on_maculateButton_clicked(self):
        """"""
        billId = self.__getBillidFromHistory()
        if billId == -1:
            return

        self.app.delete_bill(billId)
        self.updateHistoryTable()

    def __getBillidFromHistory(self):
        idx = self.ui.tableView.selectionModel().currentIndex()
        if idx.row() == -1:
            return -1

        model = self.ui.tableView.model()
        idx = model.index(idx.row(), 0)
        billId = int(model.data(idx))
        return billId

    def on_generateButton_clicked(self):
        billId = self.__getBillidFromHistory()
        if billId == -1:
            return
        bill = self.app.fetch_bill(billId)
        fileName = self.app.generate_bill(bill)
        open_file(fileName)

    @property
    def newCustomerActivated(self):
        return not self.ui.customerChooser.isEnabled()

    def showNewCustomer(self):
        if not self.newCustomerActivated:
            self.ui.customerChooser.setEnabled(False)
            self.newCustomerForm.show()
            self.ui.newCustomerButton.setText("Angra")

    def hideNewCustomer(self):
        if self.newCustomerActivated:
            self.ui.customerChooser.setEnabled(True)
            self.newCustomerForm.hide()
            self.ui.newCustomerButton.setText("Ny")

    def on_newCustomerButton_clicked(self):
        if self.newCustomerActivated:
            self.hideNewCustomer()
        else:
            self.showNewCustomer()

    def updateHistoryTable(self):
        """"""
        historyModel = QSqlQueryModel()
        self.initializeHistoryModel(historyModel)
        self.ui.tableView.setModel(historyModel)

    def initializeHistoryModel(self, model):
        model.setQuery("select id,reference,bill_date,payed,payed_date from bill")
        model.setHeaderData(0, Qt.Horizontal, "ID")
        model.setHeaderData(1, Qt.Horizontal, "Namn")
        model.setHeaderData(2, Qt.Horizontal, "Fakturan skapad")
        model.setHeaderData(3, Qt.Horizontal, "Betald")
        model.setHeaderData(4, Qt.Horizontal, "Betald Datum")
