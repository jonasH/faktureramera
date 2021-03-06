from ext.pyside2_sqlite_db import PySide2SqliteDb
import os
import pytest
from unittest.mock import Mock
import shutil


@pytest.fixture(scope="session")
def db():
    directory = os.path.dirname(__file__)
    user_settings_folder = os.path.join(directory, "..", "..", "build", "test_settings")
    shutil.rmtree(user_settings_folder, ignore_errors=True)
    os.makedirs(user_settings_folder)
    database_name = os.path.join(user_settings_folder, "testdb.sqlite")
    db = PySide2SqliteDb(database_name)
    yield db
    db.db.close()


@pytest.fixture(scope="function")
def clear_db(db):
    db.clear_all_tables()
    yield db


def test_create_customer(clear_db):
    customer_name = "viktor"
    customer = clear_db.create_customer(customer_name, "Sätra 123", "123 Gävle")
    assert customer.id == 1
    assert customer.name == customer_name


def test_fetch_customer(clear_db):
    customer_name = "viktor"
    customer = clear_db.create_customer(customer_name, "Sätra 123", "123 Gävle")
    customer2 = clear_db.fetch_customer(customer.id)

    assert customer == customer2


def test_fetch_customers(clear_db):
    customer_name = "viktor"
    customer = clear_db.create_customer(customer_name, "Sätra 123", "123 Gävle")
    customer_name = "viktor2"
    customer2 = clear_db.create_customer(customer_name, "gatan 123", "1234 valbo")
    customers = list(clear_db.fetch_customers())
    assert len(customers) == 2
    assert customer != customer2


def test_delete_bill(clear_db):
    customer_name = "viktor"
    customer = clear_db.create_customer(customer_name, "Sätra 123", "123 Gävle")
    customer_ref = "Jonas Berg"
    bill = clear_db.create_bill(customer_ref, customer.id, [])
    clear_db.delete_bill(bill.id)
    with pytest.raises(RuntimeError) as err_info:
        clear_db.fetch_bill(bill.id)
    assert "Could not fetch" in str(err_info.value)


def test_add_job(clear_db):
    customer_name = "viktor"
    customer = clear_db.create_customer(customer_name, "Sätra 123", "123 Gävle")
    customer_ref = "Jonas Berg"
    bill = clear_db.create_bill(customer_ref, customer.id, [])
    bill = clear_db.add_job(300, 4, "worki", bill)
    job = clear_db.search_jobs(bill.id)[0]
    assert job == bill.jobs[0]
    bill2 = clear_db.fetch_bill(bill.id)
    assert bill == bill2


def test_multiple_bills(clear_db):
    customer_name = "viktor"
    customer = clear_db.create_customer(customer_name, "Sätra 123", "123 Gävle")
    customer_ref = "Jonas Berg"
    bill = clear_db.create_bill(customer_ref, customer.id, [])
    bill = clear_db.add_job(300, 4, "worki", bill)
    bill2 = clear_db.create_bill(customer_ref, customer.id, [])
    bill2 = clear_db.add_job(300, 4, "worki", bill2)
    bill = clear_db.fetch_bill(bill.id)
    bill2 = clear_db.fetch_bill(bill2.id)
    assert len(bill.jobs) == 1
    assert bill != bill2


def test_update_bill_referece(clear_db):
    customer_name = "viktor"
    customer = clear_db.create_customer(customer_name, "Sätra 123", "123 Gävle")
    customer_ref = "Jonas Berg"
    bill = clear_db.create_bill(customer_ref, customer.id, [])
    reference = "Apan ola"
    bill = clear_db.update_bill(bill, reference, customer.id, [])
    bill.reference == reference


def test_update_bill_rollback(clear_db):
    customer_name = "viktor"
    customer = clear_db.create_customer(customer_name, "Sätra 123", "123 Gävle")
    customer_ref = "Jonas Berg"
    bill = clear_db.create_bill(customer_ref, customer.id, [])
    reference = "Apan ola"
    old_add_jobb = clear_db.add_job
    clear_db.add_job = Mock(side_effect=Exception)
    with pytest.raises(Exception):
        bill = clear_db.update_bill(bill, reference, customer.id, [Mock()])
    clear_db.add_job = old_add_jobb
    assert bill.reference == customer_ref
