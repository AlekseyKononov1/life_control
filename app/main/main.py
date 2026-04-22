from support_utils.logger import ILogger, Logger
from repository.guestRepository import GuestRepository
from service.validation import GuestForm

if __name__ == "__main__":
    logger = Logger()
    guestForm = GuestForm(logger)
    
    print(guestForm.validate(login="aasd123", pwd="12345"))

    
