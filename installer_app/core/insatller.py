from abc import ABC, abstractmethod


class Installer(ABC):
    @abstractmethod
    def install(self):
        pass

    @abstractmethod
    def uninstall(self):
        pass

    @abstractmethod
    def status(self):
        pass
