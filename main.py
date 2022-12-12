from joystickController import JoystickController
from flaskApp import flaskApp


if __name__ == '__main__':
    joystickController = JoystickController()
    joystickController.controller()
    #stream = flaskApp(joystickController)
    #stream.start()
