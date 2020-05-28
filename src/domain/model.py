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


@dataclass(frozen=True)
class Profile:

    daysToPay: int = 30
    address: str = "apagatan 30"
    mail: str = "joans@123.se"
    telephone: str = "070-123124"
    orgNr: str = "28934234-234"
    bankAccount: str = "235098238"
    tax: float = 0.3
    billLocation: str = "billz"
    companyName: str = "company 1"
