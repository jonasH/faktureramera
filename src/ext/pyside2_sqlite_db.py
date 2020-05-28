from interface.db import AbstractDatabase, CustomerGenerator
from domain.model import Customer, Bill, Job
from PySide2.QtSql import QSqlQuery, QSqlDatabase
from PySide2.QtCore import QDate
import os
from typing import List


def _configure_database(location: str) -> None:
    query = QSqlQuery()
    line = ""
    file_dir = os.path.dirname(__file__)
    with open(os.path.join(file_dir, "../../misc/fm.sql")) as f:
        for row in f:
            row = row.strip()
            line += row
            if row.endswith(";"):
                print(line)
                query.exec_(line)
                line = ""


class PySide2SqliteDb(AbstractDatabase):
    def __init__(self, database_name: str):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        init_db = not os.path.exists(database_name)
        self.db.setDatabaseName(database_name)
        if not self.db.open():
            raise RuntimeError(f"OMG ERROR! withz the database: {database_name}")

        if init_db:
            _configure_database(database_name)

    def clear_all_tables(self):
        query = QSqlQuery()
        query.exec_("delete from bill")
        query.exec_("delete from customer")
        query.exec_("delete from jobs")

    def create_customer(self, name: str, address: str, zip_code: str) -> Customer:
        query = QSqlQuery()
        query.prepare("INSERT INTO customer(name, address, zipcode) VALUES(?, ?, ?)")
        query.addBindValue(name)
        query.addBindValue(address)
        query.addBindValue(zip_code)
        query.exec_()
        max_id_q = "select max(id) from customer"
        last_customer_q = f"select * from customer where id=({max_id_q})"
        query.exec_(last_customer_q)
        query.next()
        return _extract_customer(query)

    def fetch_customer(self, customer_id: int) -> Customer:
        query = QSqlQuery()
        query.prepare("SELECT id,name,address,zipcode FROM customer WHERE id = ?")
        query.addBindValue(customer_id)
        query.exec_()
        query.next()
        return _extract_customer(query)

    def fetch_customers(self) -> CustomerGenerator:
        query = QSqlQuery()
        query.exec_("select id,name,address,zipcode from customer")
        while query.next():
            yield _extract_customer(query)

    def create_bill(self, reference: str, customer_id: int, jobs: List[Job]) -> Bill:
        dateFormat = "yyyy-MM-dd"
        date = QDate.currentDate()
        query = QSqlQuery()
        query.prepare("INSERT INTO bill(c_id, reference, bill_date) VALUES(?, ?, ?)")
        query.addBindValue(customer_id)
        query.addBindValue(reference)
        query.addBindValue(date.toString(dateFormat))
        query.exec_()
        max_id_q = "select max(id) from bill"
        bill = self.__fetch_bill(query, max_id_q)
        for job in jobs:
            bill = self.add_job(job.price, job.number, job.text, bill)
        return bill

    def __fetch_bill(self, query, id_expr) -> Bill:
        query.prepare(
            f"select id, bill_date, reference, c_id from bill where id=({id_expr})"
        )
        query.exec_()
        if not query.next():
            raise RuntimeError(f"Could not fetch bill with id {id_expr}")

        bill = _extract_bill(query)
        customer_id = query.value(3)
        customer = self.fetch_customer(customer_id)
        bill.customer = customer
        bill.jobs = self.__fetch_jobs(query)

        return bill

    def fetch_bill(self, bill_id: int) -> Bill:
        query = QSqlQuery()
        bill = self.__fetch_bill(query, bill_id)
        return bill

    def delete_bill(self, bill_id: int) -> None:
        query = QSqlQuery()
        query.prepare("DELETE FROM bill WHERE id = ?")
        query.addBindValue(bill_id)
        query.exec_()

    def update_bill(
        self, bill: Bill, reference: str, customer_id: int, jobs: List[Job]
    ) -> Bill:
        """TODO make sure that the customer id exists
        """
        self.db.transaction()
        dateFormat = "yyyy-MM-dd"
        date = QDate.currentDate()
        query = QSqlQuery()
        query.prepare("UPDATE bill SET c_id=?, reference=?, bill_date=? WHERE id=?")
        query.addBindValue(customer_id)
        query.addBindValue(reference)
        query.addBindValue(date.toString(dateFormat))
        query.addBindValue(bill.id)

        query.exec_()
        sql = "delete from jobs where b_id='{0}'".format(bill.id)
        query.exec_(sql)
        for j in jobs:
            self.add_job(j.price, j.number, j.text, bill)
        self.db.commit()
        return self.__fetch_bill(query, bill.id)

    def add_job(self, price: float, number: int, text: str, bill: Bill) -> Bill:
        query = QSqlQuery()
        query.prepare("INSERT INTO jobs(b_id, hours, price, job) VALUES(?, ?, ?, ?)")
        query.addBindValue(bill.id)
        query.addBindValue(number)
        query.addBindValue(price)
        query.addBindValue(text)
        query.exec_()
        job = self.__fetch_job(query, "select max(id) from jobs")
        bill.add_job(job)
        return bill

    def __fetch_jobs(self, bill: Bill) -> List[Job]:
        res = []
        query = QSqlQuery()
        query.prepare("select id, hours, price, job from jobs")
        query.exec_()
        while query.next():
            res.append(_extract_job(query))
        return res

    def __fetch_job(self, query, id_expr) -> Job:
        query.prepare(f"select id, hours, price, job from jobs where id=({id_expr})")
        query.exec_()
        if not query.next():
            raise RuntimeError(f"Could not fetch job with id {id_expr}")

        job = _extract_job(query)
        return job

    def fetch_job(self, job_id: int) -> Job:
        query = QSqlQuery()
        return self.__fetch_job(query, job_id)


# Helper functions


def _extract_customer(query: QSqlQuery) -> Customer:
    customer_id = query.value(0)
    name = query.value(1)
    address = query.value(2)
    zipcode = query.value(3)
    return Customer(customer_id, name, address, zipcode)


def _extract_bill(query: QSqlQuery) -> Bill:
    bill_id = query.value(0)
    date = query.value(1)
    ref = query.value(2)
    return Bill(bill_id, ref, date)


def _extract_job(query: QSqlQuery) -> Job:
    job_id = query.value(0)
    hours = query.value(1)
    price = query.value(2)
    text = query.value(3)
    return Job(price, hours, text, job_id)
