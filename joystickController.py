from djitellopy import tello
from joystick import Joystick
from time import sleep
from threading import Thread, Event

class JoystickController(Thread):

    def __init__(self,shared_bool:Event) -> None:
        self._shared_bool = shared_bool
        Thread.__init__(self, args=(self._shared_bool,))
        self._joystick = Joystick()
        self._joystick.flush_buffers()
        self._me=tello.Tello()
        self._me.connect()
        print(self._me.get_battery())
        self._me.streamon()

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

        if(cm==113):
            self._shared_bool.set()
        
        if(cm==114):
            self._shared_bool.clear()
        
        return [cm, lr, fb, ud, yv]


    def controller(self):
        while True:
            [cm, lr, fb, ud, yv] = self.getJoystickState()
            
            if(cm==111):
                self._me.send_rc_control(lr, fb, ud, yv)  
            
    def run(self):
        self.controller()    