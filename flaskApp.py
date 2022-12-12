import cv2
from flask import Flask, render_template, Response, stream_with_context, request
import sys
from time import sleep
from threading import Thread
from joystickController import JoystickController

class flaskApp(Thread):
    app = Flask('__name__')

    def __init__(self, joystickcontroller: JoystickController):
        Thread.__init__(self)
        self._joystickcontroller = joystickcontroller
        self._joystickcontroller._me.streamon()

    @app.route('/')
    def index(self):
        return render_template('index.html')

    @app.route('/video_feed')
    def video_feed(self):
        return Response(self._videostream(),mimetype='multipart/x-mixed-replace; boundary=frame')  

    def _videostream(self):
        while(True):
            if(self._joystickcontroller.land == True):
                sys.exit    
            img = self._joystickcontroller._me.get_frame_read().frame
            img = cv2.resize(img, (360,240))
            frame = cv2.imencode('.jpg',img)[1].tobytes()
            yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n')
            sleep(0.1)
    def run(self):
        self.app.run(host="192.168.0.171", port=5000)
        self._videostream()