from abc import ABC, abstractmethod
from support_utils.logger import ILogger
import re

class IValidation(ABC):
    @abstractmethod
    def validate(self, **kwargs) -> None | str: pass

class GuestForm(IValidation):
    def __init__(self, logger: ILogger=None):
        self.logger = logger
        self.LOGIN_HINT = "login: a-z[4:10] digits[0:5]" 
        self.PWD_HINT = "password: a-zA-Z!@#$%^&*()_+[5,15]"

    def validate(self, **kwargs) -> None | str:
        login = kwargs["login"]
        pwd = kwargs["pwd"]

        if not isinstance(login, str) or not isinstance(pwd, str):
            raise TypeError("login and pwd should be str")
        if len(login) == 0 or len(pwd) == 0:
            raise ValueError("login or pwd could not be empty for validation")
        
        loginPattern = r"[a-z]{4,10}\d{0,5}"
        pwdPattern = r"[a-zA-Z0-9!@#$%^&*()_+]{5,15}"

        isLoginMatch = bool(re.fullmatch(loginPattern, login))
        isPwdMatch = bool(re.fullmatch(pwdPattern, pwd))  
        if isLoginMatch and isPwdMatch:
            
            return None
        if not isLoginMatch or not isPwdMatch:
            return self.LOGIN_HINT + self.PWD_HINT


