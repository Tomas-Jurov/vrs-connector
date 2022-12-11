from djitellopy import tello
from joystick import Joystick
from time import sleep
import cv2
import time
from flask import Flask, render_template, Response, stream_with_context, request
import sys


class JoystickController():
    
    app = Flask('__name__')

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/video_feed')
    def video_feed():
        return Response(JoystickController.videostream(),mimetype='multipart/x-mixed-replace; boundary=frame')

    def __init__(self) -> None:
        self._joystick = Joystick()
        self._joystick.flush_buffers()
        self._me=tello.Tello()
        self._me.connect()
        self._me.streamon()

    def getJoystickState(self):
        [cm, lr, fb, ud, yv] = self._joystick.tuple


        if(cm==110):
            success = self._me.takeoff()
            print('takeoff')

        if(cm==112):
            success = self._me.land()
            print('landed')
            if(success):
                sys.exit()


        return [cm, lr, fb, ud, yv]


    def controller(self):
        while True:
            [cm, lr, fb, ud, yv] = self.getJoystickState()
            
            if(cm==111):
                self._me.send_rc_control(lr, fb, ud, yv)    

    @staticmethod
    def videostream(self):
        while(True):
            img = self._me.get_frame_read().frame
            img = cv2.resize(img, (360,240))
            frame = cv2.imencode('.jpg',img)[1].tobytes()
            yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n')
            time.sleep(0.1)
