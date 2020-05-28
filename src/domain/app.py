from typing import Generator, List
from domain.model import Customer, Bill, Job

CustomerGenerator = Generator[Customer, None, None]


class FM(object):
    def __init__(self, db, generate_bill):
        self.generate_bill = generate_bill
        self.db = db

    def fetch_customers(self) -> CustomerGenerator:
        yield from self.db.fetch_customers()

    def create_customer(self, name: str, address: str, zip_code: str) -> Customer:
        return self.db.create_customer(name, address, zip_code)

    def fetch_customer(self, customer_id: int) -> Customer:
        return self.db.fetch_customer(customer_id)

    def create_bill(self, reference: str, customer_id: int, jobs: List[Job]) -> Bill:
        return self.db.create_bill(reference, customer_id, jobs)

    def fetch_bill(self, bill_id: int) -> Bill:
        return self.db.fetch_bill(bill_id)

    def delete_bill(self, bill_id: int) -> None:
        self.db.delete_bill(bill_id)

    def update_bill(
        self, bill_id: int, reference: str, customer_id: int, jobs: List[Job]
    ) -> Bill:
        bill = self.db.fetch_bill(bill_id)
        return self.db.update_bill(bill, reference, customer_id, jobs)

    def add_job(self, price: float, number: int, text: str, bill: Bill) -> Bill:
        return self.db.add_job(price, number, text, bill)

    def fetch_job(self, job_id: int) -> Job:
        return self.db.fetch_job(job_id)
