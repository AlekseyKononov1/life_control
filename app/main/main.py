from support_utils.logger import ILogger, Logger
from repository.guestRepository import GuestRepository
from service.validation import GuestForm
from support_utils.duration import IDuration, Duration
from repository.userRepository import UserRepository

if __name__ == "__main__":
    logger = Logger()
    ur = UserRepository(logger)

    ur.writeData("db/etalon.csv", ["test1", "test2"])
    data = ur.readData("db/etalon.csv")
    print(data)


    
