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
        self.dayNameRE = re.compile(r"^[a-z]{,3};")
        self.remarkRE = re.compile(r"remark:.*")
        self.durationsRE = re.compile(r"durations:.*;")
        self.durationsCleanRE = re.compile(r"(durations:|;|\s)*")

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
        self.logger.info("New day was created")

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
        class path:
            etalon = "db/etalon.csv"
            userWeek = "db/userWeek.csv"

        etalon = self.userRepo.readData(path.etalon)
        userWeek = self.userRepo.readData(path.userWeek)
        etalon = {self.dayNameRE.search(day).group():day for day in etalon}
        userWeek = {self.dayNameRE.search(day).group():day for day in userWeek}

        for etalonDayName, etaloneWholeDay in etalon.items():
            if etalonDayName in userWeek:
                etalonDurations = self.durationsRE.search(etaloneWholeDay).group()
                userDurations = self.durationsRE.search(userWeek[etalonDayName]).group()
                etalonDurations = self.durationsCleanRE.sub("", etalonDurations)
                userDurations = self.durationsCleanRE.sub("", userDurations)
                etalonDurations = [float(el) for el in etalonDurations.split(",")]
                userDurations = [float(el) for el in userDurations.split(",")]

                for ed, ud in zip(etalonDurations, userDurations):
                    if ud < ed and bool(self.remarkRE.search(userWeek[etalonDayName])) is True:
                        userWeek[etalonDayName] = self.remarkRE.sub("remark:red", userWeek[etalonDayName])
                        break
                    elif ud < ed:
                        userWeek[etalonDayName] += ";remark:red"
                        break
                    
                if bool(self.remarkRE.search(userWeek[etalonDayName])) is False:
                        userWeek[etalonDayName] += ";remark:green"
                
        etalon = [day for _,day in etalon.items()]
        userWeek = [day for _,day in userWeek.items()]
        self.userRepo.writeData(path.etalon, etalon)
        self.userRepo.writeData(path.userWeek, userWeek)
                
                






        
            
