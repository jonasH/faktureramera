from dataclasses import dataclass, field
from typing import List


@dataclass
class Job:
    price: float
    number: int
    text: str
    id: int = -1


@dataclass
class Customer:
    id: int
    name: str
    address: str
    zipcode: str


@dataclass
class Bill:
    id: int
    reference: str
    bill_date: str
    jobs: List[Job] = field(default_factory=list)
    payed: bool = False
    payed_date: str = ""
    customer: Customer = Customer(-1, "", "", "")

    def add_job(self, job):
        self.jobs.append(job)

    def remove_job(self, job):
        self.jobs.remove(job)

    @property
    def total_sum(self) -> float:
        total_sum = 0.0
        for job in self.jobs:
            total_sum += job.price * job.number
        return total_sum



@dataclass(frozen=True)
class Profile:

    days_to_pay: int = 30
    address: str = "apagatan 30"
    mail: str = "joans@123.se"
    telephone: str = "070-123124"
    org_nr: str = "28934234-234"
    bank_account: str = "235098238"
    tax: float = 0.3
    company_name: str = "company 1"


@dataclass(frozen=True)
class AppSettings:
    bill_location: str = "Bills"
