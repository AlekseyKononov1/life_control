from abc import ABC, abstractmethod
from support_utils.logger import ILogger
from repository.userRepository import IUserRepository
import re

class IUserService(ABC):
    @abstractmethod    
    def createDay(self, dbPath: str, day: str) -> None: pass
    @abstractmethod
    def getUpdatedState(self, dbPath: str) -> list[str]: pass
    @abstractmethod
    def updateDay(self, dbPath: str, newDay: str) -> None: pass
    @abstractmethod
    def deleteDay(self, dbPath: str, dayName: str) -> None: pass

class UserService(IUserService):
    def __init__(self, logger: ILogger, userRepo: IUserRepository):
        self.logger = logger
        self.userRepo = userRepo
        self.dayNameRE = re.compile(r"[a-z]{,3};")
        self.remarkRE = re.compile(r"remark:.*")

    def getUpdatedState(self, dbPath: str) -> list[str]: 
        return self.userRepo.readData(dbPath)
    
    def createDay(self, dbPath: str, day: str) -> None:
        week = self.userRepo.readData(dbPath)
        if len(week) == 0:
            self.userRepo.writeData(dbPath, [day])
            return

        newDayName = self.dayNameRE.search(day).group()
        for el in week:
            if newDayName == self.dayNameRE.search(el).group():
                return
        
        week.append(day)
        self.userRepo.writeData(dbPath, week)

    def updateDay(self, dbPath: str, newDay: str) -> None:
        week = self.userRepo.readData(dbPath)
        newDayName = self.dayNameRE.search(newDay).group()

        for i, el in enumerate(week):
            if newDayName == self.dayNameRE.search(el).group():
                week[i] = newDay
        
        self.userRepo.writeData(dbPath, week)

    def deleteDay(self, dbPath: str, dayName: str) -> None:
        week = self.userRepo.readData(dbPath)
        dayName += ";"
        
        for i, el in enumerate(week):
            if dayName == self.dayNameRE.search(el).group():
                del week[i]
                self.userRepo.writeData(dbPath, week)
                return
            
    def makeRemark(self) -> None:
        etalon = self.userRepo.readData("db/etalon.csv")
        userWeek = self.userRepo.readData("db/userWeek.csv")


        for et, uw in zip(etalon, userWeek):  
            pass 
        
            
