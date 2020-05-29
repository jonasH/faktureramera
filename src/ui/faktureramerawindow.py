import webbrowser
from PySide2.QtWidgets import QApplication, QMainWindow, QErrorMessage, QPushButton
from PySide2.QtSql import QSqlQueryModel
from PySide2.QtCore import Qt, QFile
from PySide2.QtUiTools import QUiLoader
import os
from domain.model import Job
from support import resource_path


def load_ui(filename):
    module_dir = os.path.dirname(__file__)
    module_dir = resource_path(module_dir)
    file_name = os.path.join(module_dir, filename)
    qfile = QFile(file_name)
    qfile.open(QFile.ReadOnly)
    loader = QUiLoader()
    return loader.load(qfile)


class FaktureraMeraWindow(QMainWindow):
    def __init__(self, app, parent=None):
        """"""
        super(FaktureraMeraWindow, self).__init__(parent)
        self.app = app
        self.setup_ui()
        self.updateHistoryTable()
        job = load_ui("jobform.ui")
        self.jobList = [job]
        self.ui.jobsLayout.addWidget(job)
        self.populateCustomers()
        self.newCustomerForm = load_ui("newcustomerform.ui")
        self.newCustomerForm.hide()
        self.ui.newCustomerLayout.addWidget(self.newCustomerForm)
        self.edit_bill_id = 0

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

    def populateCustomers(self) -> None:
        self.ui.customerChooser.clear()
        for c in self.app.fetch_customers():
            self.ui.customerChooser.addItem(c.name)

    def validateForSubmit(self):
        errorMsgs = []
        reference = self.ui.referenceField.text()
        if reference == "":
            errorMsgs.append("Du har glomt referensfaltet")
        counter = 1
        for j in self.jobList:

            if j.description.text() == "":
                errorMsgs.append("Du har glomt beskrivning pa job " + str(counter))
            try:
                float(j.price.text().replace(",", "."))
            except Exception:
                errorMsgs.append(
                    "Det ser inte ut som en siffra pa priset pa job " + str(counter)
                )
            try:
                int(j.number.text())
            except Exception:
                errorMsgs.append(
                    "Det ser inte ut som en siffra pa antalet pa job " + str(counter)
                )
            counter += 1
        if self.newCustomerActivated:
            if self.newCustomerForm.name.text() == "":
                errorMsgs.append("Det finns inget namn pa den nya kunden")
            if self.newCustomerForm.address.text() == "":
                errorMsgs.append("Det finns ingen address pa den nya kunden")
            if self.newCustomerForm.zip.text() == "":
                errorMsgs.append("Det finns inget postnummer pa den nya kunden")

        if len(errorMsgs) != 0:
            errWidget = QErrorMessage(self)
            errWidget.showMessage("<br/>".join(errorMsgs))
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
                self.on_addJobButton_clicked()
            job = self.jobList[-1]
            job.description.setText(j.text)
            job.number.setText(str(j.number))
            job.price.setText(str(j.price))

    def reinitUI(self):
        self.edit_bill_id = 0
        self.ui.saveGenerateButton.setText("Generera")
        numberOfJobs = len(self.jobList)
        for i in range(numberOfJobs):
            self.removeJobWidget()
        self.on_addJobButton_clicked()
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
        if not self.validateForSubmit():
            return

        customer = self.__current_customer()
        customer_id = customer.id
        reference = self.ui.referenceField.text()
        jobs = []
        for j in self.jobList:
            text = j.description.text()
            price = float(j.price.text().replace(",", "."))
            number = int(j.number.text())
            jobs.append(Job(price, number, text))

        if self.edit_bill_id == 0:
            bill = self.app.create_bill(reference, customer_id, jobs)

        else:
            bill = self.app.update_bill(self.edit_bill_id, reference, customer_id, jobs)

        fileName = self.app.generate_bill(bill)
        self.reinitUI()
        self.updateHistoryTable()
        self.populateCustomers()
        webbrowser.open(fileName)

    def removeJobWidget(self):
        job = self.jobList[-1]
        job.hide()
        self.ui.jobsLayout.removeWidget(job)
        QApplication.processEvents()
        self.jobList.remove(job)

    def on_addJobButton_clicked(self):
        job = load_ui("jobform.ui")
        self.ui.jobsLayout.addWidget(job)
        self.jobList.append(job)
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
        webbrowser.open(fileName)

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
