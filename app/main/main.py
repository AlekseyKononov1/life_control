from support_utils.logger import ILogger, Logger
from repository.guestRepository import GuestRepository
from service.validation import GuestForm
from support_utils.duration import IDuration, Duration

if __name__ == "__main__":
    durations = [Duration("2.30"), Duration("2.40"), Duration("2.50")]
    # 8
    print(Duration("0.0").getSum(durations)) 


    
