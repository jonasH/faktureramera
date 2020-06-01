from typing import Generator, List
from domain.model import Customer, Bill, Job, Profile
import os
from interface.settings_if import AbstractSettings
from interface.db import AbstractDatabase

CustomerGenerator = Generator[Customer, None, None]


class FM(object):
    def __init__(self, db: AbstractDatabase, generate_bill, settings: AbstractSettings):
        self.__generate_bill = generate_bill
        self.db = db
        self.settings = settings

    def generate_bill(self, bill: Bill) -> str:
        app_settings = self.settings.app_settings()
        settings_folder = self.settings.settings_folder()
        location = os.path.join(settings_folder, app_settings.bill_location)
        profile = self.settings.profile()
        return self.__generate_bill(bill, location, profile)

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

    def shut_down(self):
        self.settings.save()
