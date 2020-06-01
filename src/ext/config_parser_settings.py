"""
[profile]
    days_to_pay: int = 30
    address: str = "apagatan 30"
    mail: str = "joans@123.se"
    telephone: str = "070-123124"
    org_nr: str = "28934234-234"
    bank_account: str = "235098238"
    tax: float = 0.3
    company_name: str = "company 1"
[app_settings]
    bill_location: str = "billz"

"""
from configparser import ConfigParser
from interface.settings_if import AbstractSettings
import os
from domain.model import Profile, AppSettings

CONF_FILE_NAME = "fm.ini"


def _configure_base_settings(config: ConfigParser) -> None:
    config["Profile"] = {
        "days_to_pay": "30",
        "address": "apagatan 30",
        "mail": "joans@123.se",
        "telephone": "070-123124",
        "org_nr": "28934234-234",
        "bank_account": "235098238",
        "tax": "0.3",
        "company_name": "company 1",
    }
    config["app_settings"] = {"bill_location": "Bills"}


class ConfigParserSettings(AbstractSettings):
    def __init__(self, settings_path: str):
        self.config = ConfigParser()
        self.__settings_path = settings_path
        conf_path = os.path.join(settings_path, CONF_FILE_NAME)
        if not os.path.exists(conf_path):
            self.__start_new_config()
        else:
            self.__read_existing_config(conf_path)

    def __start_new_config(self) -> None:
        if not os.path.exists(self.__settings_path):
            os.mkdir(self.__settings_path)
        _configure_base_settings(self.config)
        self.save()

    def __read_existing_config(self, conf_path: str) -> None:
        with open(conf_path) as f:
            self.config.read_file(f)

    def save(self) -> None:
        config_path = os.path.join(self.__settings_path, CONF_FILE_NAME)
        with open(config_path, "w") as configfile:
            self.config.write(configfile)

    def settings_folder(self) -> str:
        return self.__settings_path

    def profile(self) -> Profile:
        profile = self.config["Profile"]
        days_to_pay = profile.getint("days_to_pay")
        address = profile["address"]
        mail = profile["mail"]
        telephone = profile["telephone"]
        org_nr = profile["org_nr"]
        bank_account = profile["bank_account"]
        tax = profile.getfloat("tax")
        company_name = profile["company_name"]
        return Profile(
            days_to_pay,
            address,
            mail,
            telephone,
            org_nr,
            bank_account,
            tax,
            company_name,
        )

    def app_settings(self) -> AppSettings:
        bill_location = self.config["app_settings"]["bill_location"]
        return AppSettings(bill_location)
