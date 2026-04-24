from abc import ABC, abstractmethod

class IUser(ABC):
    @abstractmethod
    def createDay(day: dict[str, dict[str, list[str | IDuration]]]) ->  bool: pass