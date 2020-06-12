from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QErrorMessage,
    QPushButton,
    QCompleter,
)
from PySide2.QtSql import QSqlQueryModel
from PySide2.QtCore import (
    Qt,
    QFile,
    QObject,
    QEvent,
    QSettings,
    QCoreApplication,
)
from PySide2.QtUiTools import QUiLoader
import os
from domain.model import Job, Profile
from support import resource_path
import platform
from typing import List
import subprocess
from functools import partial
from ui.faktureramera import Ui_MainWindow


def load_ui(filename):
    module_dir = os.path.dirname(__file__)
    module_dir = resource_path(module_dir)
    file_name = os.path.join(module_dir, filename)
    qfile = QFile(file_name)
    qfile.open(QFile.ReadOnly)
    loader = QUiLoader()
    loader.setLanguageChangeEnabled(True)
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
        return QObject.eventFilter(self, obj, event)


class FaktureraMeraWindow(QMainWindow):
    def __init__(self, app, translator, parent=None, load_data=True):
        super(FaktureraMeraWindow, self).__init__(parent)
        self.translator = translator
        self.app = app
        self.edit_bill_id = 0
        self.tab_new_job_filter = NewJobFilter(self)
        self.jobList = []
        self.__last_jobs = self.app.search_jobs(20)
        self.setup_ui()
        self.load_settings()
        if load_data:
            self.load_data()

    def load_settings(self):
        settings = QSettings("JH Code Factory", "FaktureraMera")
        tab_index = int(settings.value("MainWindow/tab", 0))
        self.ui.tabWidget.setCurrentIndex(tab_index)
        current_lang = settings.value("Application/lang", "se_SE")
        self.ui.language_chooser.setCurrentText(current_lang)
        self.install_language(current_lang)

    def install_language(self, lang):
        QApplication.removeTranslator(self.translator)
        module_dir = os.path.dirname(__file__)
        path = resource_path(f"{module_dir}/i18n/{lang}")
        self.translator.load(path)
        QApplication.installTranslator(self.translator)

    def save_settings(self):
        settings = QSettings("JH Code Factory", "FaktureraMera")
        settings.setValue("MainWindow/tab", self.ui.tabWidget.currentIndex())
        settings.setValue("Application/lang", self.ui.language_chooser.currentText())

    def closeEvent(self, event):
        self.save_settings()
        event.accept()

    def load_data(self):
        self.updateHistoryTable()
        self.populateCustomers()
        self.load_settings_data()
        self.load_settings()

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

    def on_language_changed(self, index):
        lang = self.ui.language_chooser.currentText()
        self.install_language(lang)
        self.ui.retranslateUi(self)

    def setup_ui(self) -> None:
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        lang = self.ui.language_chooser
        lang.addItems(["en_US", "se_SE"])
        lang.currentIndexChanged.connect(self.on_language_changed)
        btn = self.findChild(QPushButton, "new_customer_button")
        btn.clicked.connect(self.on_new_customer_button_clicked)
        btn = self.findChild(QPushButton, "cancel_customer_button")
        btn.clicked.connect(self.on_cancel_customer_button_clicked)
        btn = self.findChild(QPushButton, "generate_button")
        btn.clicked.connect(self.on_generate_button_clicked)
        btn = self.findChild(QPushButton, "update_button")
        btn.clicked.connect(self.on_update_button_clicked)
        btn = self.findChild(QPushButton, "zeroButton")
        btn.clicked.connect(self.on_zeroButton_clicked)
        btn = self.findChild(QPushButton, "editBillButton")
        btn.clicked.connect(self.on_editBillButton_clicked)
        btn = self.findChild(QPushButton, "addJobButton")
        btn.clicked.connect(self.on_addJobButton_clicked)
        btn = self.findChild(QPushButton, "removeJobButton")
        btn.clicked.connect(self.on_removeJobButton_clicked)
        btn = self.findChild(QPushButton, "maculateButton")
        btn.clicked.connect(self.on_maculateButton_clicked)
        btn = self.findChild(QPushButton, "generateButton")
        btn.clicked.connect(self.on_generateButton_clicked)
        btn = self.findChild(QPushButton, "open_bills_btn")
        btn.clicked.connect(self.on_open_bills)
        btn = self.findChild(QPushButton, "save_profile_btn")
        btn.clicked.connect(self.on_save_profile)
        self.ui.generate_button.show()
        self.ui.update_button.hide()
        self.newCustomerForm = load_ui("newcustomerform.ui")
        self.hideNewCustomer()
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
            err_msg = QCoreApplication.translate(
                "main", "Description is empty for job {counter}"
            )
            err_msg.format(counter=counter)
            error_msgs.append(err_msg)
        if j.price.value() == 0.0:
            err_msg = QCoreApplication.translate(
                "main", "Price is zero for job {counter}"
            )
            err_msg.format(counter=counter)
            error_msgs.append(err_msg)
        if j.number.value() == 0:
            err_msg = QCoreApplication.translate(
                "main", "Number is zero for job {counter}"
            )
            err_msg.format(counter=counter)
            error_msgs.append(err_msg)
        return error_msgs

    def __validate_new_customer(self) -> List[str]:
        err_msgs = []
        if self.newCustomerForm.name.text() == "":
            err_msgs.append(
                QCoreApplication.translate("main", "No name for the new customer")
            )
        if self.newCustomerForm.address.text() == "":
            err_msgs.append(
                QCoreApplication.translate("main", "No address for the new customer")
            )
        if self.newCustomerForm.zip.text() == "":
            err_msgs.append(
                QCoreApplication.translate("main", "No zip code for the new customer")
            )
        return err_msgs

    def validate_for_submit(self):
        error_msgs = []
        reference = self.ui.referenceField.text()
        if reference == "":
            error_msgs.append(
                QCoreApplication.translate(
                    "main", "You have forgotten the reference field"
                )
            )

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
        self.ui.generate_button.hide()
        self.ui.update_button.show()

    def poulateBillData(self, bill):
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
        self.ui.generate_button.show()
        self.ui.update_button.hide()

        numberOfJobs = len(self.jobList)
        for i in range(numberOfJobs):
            self.removeJobWidget()
        self.__last_jobs = self.app.search_jobs(20)

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

    def on_update_button_clicked(self):
        self.save_and_generate_bill()

    def on_generate_button_clicked(self):
        self.save_and_generate_bill()

    def save_and_generate_bill(self):
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

    def __completion_selected(self, job_text: str, job_widget):
        job_data = self.__last_jobs[job_text]
        job_widget.price.setValue(job_data.price)
        job_widget.price.setFocus()

    def add_job_widget(self,):
        if len(self.jobList) > 0:
            self.jobList[-1].number.removeEventFilter(self.tab_new_job_filter)
        job = load_ui("jobform.ui")
        names = list(self.__last_jobs.keys())
        completer = QCompleter(names)
        ev_handler = partial(self.__completion_selected, job_widget=job)
        completer.activated.connect(ev_handler)
        job.description.setCompleter(completer)
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
        self.ui.customerChooser.setEnabled(False)
        self.newCustomerForm.show()
        self.ui.cancel_customer_button.show()
        self.ui.new_customer_button.hide()

    def hideNewCustomer(self):
        self.ui.customerChooser.setEnabled(True)
        self.newCustomerForm.hide()
        self.ui.cancel_customer_button.hide()
        self.ui.new_customer_button.show()

    def on_new_customer_button_clicked(self):
        self.showNewCustomer()

    def on_cancel_customer_button_clicked(self):
        self.hideNewCustomer()

    def updateHistoryTable(self):
        historyModel = QSqlQueryModel()
        self.ui.tableView.setModel(historyModel)
        self.initializeHistoryModel(historyModel)

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            self.retranslateUI()

    def retranslateUI(self):
        model = self.ui.tableView.model()
        model.setHeaderData(0, Qt.Horizontal, QCoreApplication.translate("main", "ID"))
        model.setHeaderData(
            1, Qt.Horizontal, QCoreApplication.translate("main", "Name")
        )
        model.setHeaderData(
            2, Qt.Horizontal, QCoreApplication.translate("main", "Created")
        )
        model.setHeaderData(
            3, Qt.Horizontal, QCoreApplication.translate("main", "Payed")
        )
        model.setHeaderData(
            4, Qt.Horizontal, QCoreApplication.translate("main", "Payed Date")
        )

    def initializeHistoryModel(self, model):
        model.setQuery("select id,reference,bill_date,payed,payed_date from bill")
        self.retranslateUI()
