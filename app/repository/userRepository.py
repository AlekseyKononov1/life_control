from abc import ABC, abstractmethod
from support_utils.logger import ILogger

class IUserRepository(ABC):
    @abstractmethod
    def readData(self, dbPath: str) -> list[str] | None: pass
    @abstractmethod
    def writeData(self, dbPath: str, data: list[str]) -> bool: pass

class UserRepository(IUserRepository):
    def __init__(self, logger: ILogger=None):
        self.logger = logger
        self.setup()
    
    def setup(self) -> None:
        try:
            with open("db/etalon.csv", "a", encoding="utf-8"): pass
            with open("db/userWeek.csv", "a", encoding="utf-8"): pass
        except OSError as ose:
            self.logger.error(f"You need to give access to OS for setup this application ~ {ose}")

        return None

    def readData(self, dbPath: str) -> list[str] | None: 
        try:
            with open(dbPath, "r", encoding="utf-8") as f:
                data = f.readlines()
            data = [d[:len(d)-1] for d in data if d != "" and len(d) != 1]
        except OSError as ose:
            self.logger.error(f"Check permissions and existence for {dbPath} ~ {ose}")
            return None
        
        return data

    def writeData(self, dbPath: str, data: list[str]) -> bool:
        data = [f"{d}\n" for d in data]
        try:
            with open(dbPath, "w", encoding="utf-8") as f:
                 f.writelines(data)
            return True
        except OSError as ose:
            self.logger.error(f"Check permissions and existence for {dbPath} ~ {ose}")
            return False
        
