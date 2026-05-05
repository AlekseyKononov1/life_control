from support_utils.logger import ILogger, Logger
from repository.guestRepository import GuestRepository
from repository.userRepository import UserRepository
from service.validation import GuestForm
from support_utils.duration import IDuration, Duration
from repository.userRepository import UserRepository
from controller.userController import IUserController, UserController
from service.userService import UserService
import sys
from ui_component.userUIComponent import QApplication, MainWindow

def run():
    logger = Logger()
    userRepository = UserRepository(logger)
    userService = UserService(logger, userRepository)
    userController = UserController(userService)

    app = QApplication(sys.argv)
    window = MainWindow(userController)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()


