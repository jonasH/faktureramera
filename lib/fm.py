from PySide2.QtSql import QSqlQuery
from PySide2.QtCore import QDate
import logging
import lib.fakturamodel as model


def __calc_next_id(query: QSqlQuery, table: str) -> int:
    query.exec_(f"select max(id) from {table}")
    query.next()
    max_id = query.record().value(0)
    if max_id == "" or max_id is None:
        max_id = 0
    return max_id + 1


def create_customer(name: str, address: str, zip_code: str) -> QSqlQuery:
    query = QSqlQuery()
    new_id = __calc_next_id(query, 'customer')
    query.prepare("INSERT INTO customer VALUES(?, ?, ?, ?)")
    query.addBindValue(new_id)
    query.addBindValue(name)
    query.addBindValue(address)
    query.addBindValue(zip_code)
    if not query.exec_():
        logging.error("Could not create new customer.")

    return fetch_customer(new_id)


def fetch_customer(customer_id: int) -> model.Customer:
    query = QSqlQuery()
    query.prepare("SELECT * FROM customer WHERE id = ?")
    query.addBindValue(customer_id)
    query.exec_()
    query.next()
    return extract_customer(query)
    

def extract_customer(query: QSqlQuery) -> model.Customer:
    customer_id = query.value(0)
    name = query.value(1)
    address = query.value(2)
    zipcode = query.value(3)
    return model.Customer(customer_id, name, address, zipcode)

    
def create_bill(reference: str, customer_id: int) -> model.Bill:
    """"""
    dateFormat = "yyyy-MM-dd"
    date = QDate.currentDate()
    query = QSqlQuery()
    next_id = __calc_next_id(query, 'bill')
    query.prepare("INSERT INTO bill VALUES(?, ?, ?, ?, 0, NULL)")
    query.addBindValue(next_id)
    query.addBindValue(customer_id)
    query.addBindValue(reference)
    query.addBindValue(date.toString(dateFormat))
    if not query.exec_():
        logging.error("Could not create new bill.")

    return fetch_bill(next_id)


def update_bill(bill_id: int, reference: str, customer_id: int) -> model.Bill:
    dateFormat = "yyyy-MM-dd"
    date = QDate.currentDate()
    query = QSqlQuery()
    query.prepare("UPDATE bill SET c_id=?, reference=?, bill_date=? WHERE id=?")
    query.addBindValue(customer_id)
    query.addBindValue(reference)
    query.addBindValue(date.toString(dateFormat))
    query.addBindValue(bill_id)

    query.exec_()
    sql = "delete from jobs where b_id='{0}'".format(bill_id)
    query.exec_(sql)
    return fetch_bill(bill_id)
    

def fetch_bill(bill_id: int) -> model.Customer:
    query = QSqlQuery()
    query.prepare("SELECT id, c_id, reference, bill_date FROM bill WHERE id = ?")
    query.addBindValue(bill_id)
    if query.exec_():
        raise RuntimeError(f"Could not fetch bill with id {bill_id}")
    query.next()
    bill = extract_bill(query)
    customer_id = query.value(1)
    customer = fetch_customer(customer_id)
    bill.setCustomer(customer)
    jobs = extract_jobs(query)
    for j in jobs:
        bill.addJob(j)
    return 


def delete_bill(bill_id: int) -> None:
    """"""
    query = QSqlQuery()
    query.prepare("DELETE FROM bill WHERE id = ?")
    query.addBindValue(bill_id)
    if not query.exec_():
        logging.error(f"Could not delete bill with id {bill_id}")


def extract_bill(query: QSqlQuery) -> model.Bill:
    bill_id = query.value(0)
    date = query.value(3)
    ref = query.value(2)
    return model.Bill(bill_id, ref, date)


def new_job(price: float, number: int, text: str, bill_id: int) -> model.Job:
    query = QSqlQuery()
    next_id = __calc_next_id(query, 'jobs')
    query.prepare("INSERT INTO jobs VALUES(?, ?, ?, ?, ?)")
    query.addBindValue(next_id)
    query.addBindValue(bill_id)
    query.addBindValue(number)
    query.addBindValue(price)
    query.addBindValue(text)
    if not query.exec_():
        logging.error("Could not create new job.")
    
    return fetch_job(next_id)


def fetch_job(job_id: int) -> model.Job:
    query = QSqlQuery()
    query.prepare("SELECT hours, price, job FROM jobs WHERE id = ?")
    query.addBindValue(job_id)
    if not query.exec_():
        logging.error(f"Could not fetch job {job_id}.")
    query.next()
    return extract_job(query)


def fetch_jobs(args):
    query = QSqlQuery()
    query.exec_("SELECT hours, price, job FROM jobs ORDER BY id")
    return extract_jobs(query)


def extract_jobs(query: QSqlQuery):
    """"""
    result = []
    while query.next():
        result.append(extract_job(query))

    return result


def extract_job(query: QSqlQuery) -> model.Job:
    price = query.value(1)
    hours = query.value(0)
    text = query.value(2)
    return model.Job(price, hours, text)
