import abc
from domain.model import Profile, AppSettings


class AbstractSettings(abc.ABC):
    @abc.abstractmethod
    def save(self) -> None:
        pass

    @abc.abstractmethod
    def profile(self) -> Profile:
        pass

    @abc.abstractmethod
    def save_profile(self, profile: Profile) -> None:
        pass

    @abc.abstractmethod
    def app_settings(self) -> AppSettings:
        pass

    @abc.abstractmethod
    def settings_folder(self) -> str:
        pass
