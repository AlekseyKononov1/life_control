from abc import ABC, abstractmethod
from datetime import datetime
import os
import traceback


class ILogger(ABC):
    @abstractmethod
    def info(self, record: str) -> bool: pass
    @abstractmethod
    def error(self, record: str) -> bool: pass
    @abstractmethod
    def setup(self, path: str) -> bool: pass


class Logger(ILogger):
    def __init__(self, folderPath: str="./../logs", logFileName: str="/app.log"):
        self.ERROR_PATTERN = "~~~ERROR"
        self.INFO_PATTERN = "INFO"
        self.logFilePath = None

        try:
            if not isinstance(folderPath, str) or not isinstance(logFileName, str):
                raise TypeError("logger should be initialized with str args")
            if len(folderPath) == 0 or len(logFileName) == 0:
                raise ValueError("logger should be initialized with correct str values")

            self.logFilePath = folderPath + logFileName   
            if not self.setup(folderPath):
                raise Exception("logger setup not succeed")
        except TypeError as te:
            self.printExceptionWithTrace(te)
        except ValueError as ve:
            self.printExceptionWithTrace(ve)
        except Exception as e:
            self.printExceptionWithTrace(e)

    def setup(self, path: str) -> bool:
        try:
            os.makedirs(path, exist_ok=True)
        except OSError:
            raise OSError(f"Could not create folder for logs: path={path}")
        
        with open(self.logFilePath, "a", encoding="utf-8") as f:
            pass

        return True
    
    def info(self, record: str) -> bool:
        dtNow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.logFilePath, "a", encoding="utf-8") as f:
            f.write(f"\n{self.INFO_PATTERN};{dtNow};{record}")
        return True
        
    def error(self, record: str) -> bool:
        dtNow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open (self.logFilePath, "a", encoding="utf-8") as f:
            f.write(f"\n{self.ERROR_PATTERN};{dtNow};{record}")
        return True

    def printExceptionWithTrace(self,exceptionMsg: str) -> None:
        print(exceptionMsg)
        traceback.print_exc()
