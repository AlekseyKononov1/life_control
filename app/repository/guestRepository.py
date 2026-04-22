from general_interface.guest import IGuest
from os import makedirs
from support_utils.logger import ILogger

class GuestRepository(IGuest):
    def __init__(self, dbFolder: str="./db", credFile: str="/credentials.csv", logger: ILogger = None):
        self.dbFolder = dbFolder
        self.credFile = credFile
        self.logger = logger

        self.setup()

    def setup(self):
        makedirs(self.dbFolder, exist_ok=True)
        with open(self.dbFolder + self.credFile, "a", encoding="utf-8") as f:
            pass
    
    def isCorrectGuestCreds(self, login: str, pwd: str) -> bool:
        with open(self.dbFolder + self.credFile, "r", encoding="utf-8") as f:
            dbCreds = f.readlines()
        
        dbCreds = filter(lambda x: x is not None and x != "", map(lambda x: x[:len(x)-1], dbCreds))
        for cred in dbCreds:
            dbLogin, dbPwd =  cred.split(";")
            if dbLogin == login and dbPwd == pwd:
                return True
        
        return False

    def signIn(self, login: str, pwd: str) -> bool:
        try:
            if not self.isCorrectGuestCreds(login, pwd):
                return False
        except OSError:
            self.logger.error(f"User {login} got OS error with file {self.dbFolder + self.credFile}")
            return False
        
        self.logger.info(f"User {login} is successfuly made sign in")
        return True

    def signUp(self, login: str, pwd: str) -> bool:
        try:
            with open(self.dbFolder + self.credFile, "a", encoding="utf-8") as f:
                creds = f"{login};{pwd}\n"
                f.write(creds)
            self.logger.info(f"User with name {login} made sign up")
            return True
        except OSError:
            self.logger.error(f"User {login} got OS error with file {self.dbFolder + self.credFile}")
            return False
        