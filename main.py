import threading
from joystickController import JoystickController

joystickController = JoystickController()

thread1 = threading.Thread(target=joystickController.controller())
thread1.start()

thread2 = threading.Thread(target=joystickController.videostream())
thread2.start()



if __name__ == '__main__':
    joystickController.app.run(host="192.168.0.171", port=5000)
