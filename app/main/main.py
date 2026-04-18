from support_utils.logger import ILogger, Logger
from repository.guestRepository import GuestRepository

if __name__ == "__main__":
    logger = Logger()
    guestRepository = GuestRepository(logger=logger)

    print(guestRepository.signUp("admin", "admin"))
    print(guestRepository.signIn("admin", "admin"))

    
