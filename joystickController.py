from djitellopy import tello
from joystick import Joystick
from time import sleep
#from threading import Thread

class JoystickController():

    def __init__(self) -> None:
        #Thread.__init__(self)
        self._joystick = Joystick()
        self._joystick.flush_buffers()
        self._me=tello.Tello()
        self._me.connect()

    def getJoystickState(self):
        [cm, lr, fb, ud, yv] = self._joystick.tuple


        if(cm==110):
            success = self._me.takeoff()
            if(success):
                self._joystick._serial.write(b'\x01')
            print('takeoff')

        if(cm==112):
            success = self._me.land()
            if(success):
                self._joystick._serial.write(b'\x01')
            print('landed')



        return [cm, lr, fb, ud, yv]


    def controller(self):
        while True:
            [cm, lr, fb, ud, yv] = self.getJoystickState()
            
            if(cm==111):
                self._me.send_rc_control(lr, fb, ud, yv)  
            else:
                self._me.send_rc_control(0,0,0,0)
    # def run(self):
    #     self.controller()    