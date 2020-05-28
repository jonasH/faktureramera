import abc
from domain.model import Customer, Bill, Job
from typing import Generator, List

CustomerGenerator = Generator[Customer, None, None]


class AbstractDatabase(abc.ABC):
    @abc.abstractmethod
    def create_customer(self, name: str, address: str, zip_code: str) -> Customer:
        pass

    @abc.abstractmethod
    def fetch_customers(self) -> CustomerGenerator:
        pass

    @abc.abstractmethod
    def fetch_customer(self, customer_id: int) -> Customer:
        pass

    @abc.abstractmethod
    def create_bill(self, reference: str, customer_id: int, jobs: List[Job]) -> Bill:
        pass

    @abc.abstractmethod
    def fetch_bill(self, bill_id: int) -> Bill:
        pass

    @abc.abstractmethod
    def delete_bill(self, bill_id: int) -> None:
        pass

    @abc.abstractmethod
    def update_bill(
        self, bill: Bill, reference: str, customer_id: int, jobs: List[Job]
    ) -> Bill:
        pass

    @abc.abstractmethod
    def add_job(self, price: float, number: int, text: str, bill: Bill) -> Bill:
        pass

    @abc.abstractmethod
    def fetch_job(self, job_id: int) -> Job:
        pass
