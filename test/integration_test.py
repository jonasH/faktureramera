import pytest
import os
from lib.db import openDatabase
from lib.fm import create_customer, create_bill, update_bill, new_job, delete_bill


@pytest.fixture(autouse=True)
def setup_test_database():
    database_path = "test_fm.sqlite"
    if os.path.exists(database_path):
        os.unlink(database_path)
    openDatabase(database_path)
    yield



def test_alot():
    customer = create_customer("jonas", "soerby", "802 55")
    assert customer.name == "jonas"
    bill = create_bill("someone", customer.id)
    assert bill.reference == "someone"
    bill2 = update_bill(bill.id, "someoneelse", customer.id)
    assert bill2.reference == "someoneelse"
    job = new_job(12, 13, "ASDF", bill2.id)
    
    assert job.price == 12
    assert job.number == 13
    assert job.text == "ASDF"

    delete_bill(bill2.id)

    with pytest.raises(RuntimeError):
        fetch_bill(bill2.id)
