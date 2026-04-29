from abc import ABC, abstractmethod
from service.userService import IUserService

class IUserController(ABC):
    @abstractmethod
    def readData(self, dbPath: str) -> list[str] | None: pass
    @abstractmethod
    def writeData(self, dbPath: str, data: list[str]) -> None: pass
    @abstractmethod
    def makeRemark(self) -> None: pass

class UserController(IUserController):
    def __init__(self, service: IUserService):
        self.service = service

    def readData(self, dbPath: str) -> list[str] | None:
        self.makeRemark()
        return self.service.readData(dbPath)

    def writeData(self, dbPath: str, data: list[str]) -> None: 
        self.service.writeData(dbPath, data)

    def makeRemark(self) -> None: 
        self.service.makeRemark()