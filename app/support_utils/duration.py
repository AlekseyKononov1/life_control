from abc import ABC, abstractmethod

class IDuration(ABC):
    @abstractmethod
    def getSum(self, durations: list['IDuration']) -> 'IDuration': pass
    @abstractmethod
    def initDuration(self, duration: str) -> tuple[int,int]: pass


class Duration(IDuration):
    def __init__(self, duration: str=None) -> None:
        if not isinstance(duration, str):
            raise TypeError("Duration should be instantiated with str type")
        
        self.Hours, self.Minutes = self.initDuration(duration)
        isValidValue = (
            len(duration) <= 5
            and self.Hours >= 0
            and self.Minutes >= 0
            and self.Minutes <= 60
        )
        if not isValidValue:
            raise ValueError("Not valid value for Duration instantiation")
        

    def initDuration(self, duration: str) -> tuple[int,int]:
        separatedHnM = map(lambda x: int(x), duration.split("."))
        return tuple(separatedHnM)
    
    def getSum(self, durations: list[IDuration]) -> IDuration:
        result = Duration("0.0")
        
        for duration in durations:
            result.Hours += duration.Hours
            result.Minutes += duration.Minutes
        
        result.Hours += result.Minutes // 60
        result.Minutes = result.Minutes % 60

        return result
    
    def __repr__(self):
        return f"{self.Hours}:{self.Minutes}"
    
