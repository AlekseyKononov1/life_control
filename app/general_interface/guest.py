from abc import ABC, abstractmethod

class IGuest(ABC):
    @abstractmethod
    def signIn(self, login: str, pwd: str) -> bool: pass
    @abstractmethod
    def signUp(self, login: str, pwd: str) -> bool: pass
