from djitellopy import tello
from joystick import Joystick
from time import sleep

class JoystickController():

    def __init__(self) -> None:
        self._joystick = Joystick()
        self._joystick.flush_buffers()
        self._me=tello.Tello()
        self._me.connect()

    def getJoystickState(self):
        [cm, lr, fb, ud, yv] = self._joystick.tuple


        if(cm==110):
            success = self._me.takeoff()
            print(success)
            print('takeoff')

        if(cm==112):
            success = self._me.land()
            print(success)
            print('landed')



        return [cm, lr, fb, ud, yv]


    def controller(self):
        while True:
            [cm, lr, fb, ud, yv] = self.getJoystickState()
            
            if(cm==111):
                self._me.send_rc_control(lr, fb, ud, yv)  
            else:
                self._me.send_rc_control(0,0,0,0)
