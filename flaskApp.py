import cv2
from flask import Flask, render_template, Response, stream_with_context, request
from time import sleep
from joystickController import JoystickController
from threading import Thread

joystick_controller = JoystickController()

app = Flask('__name__')

@app.route('/')
def index():
    return render_template('index.html')

def stream():
    while(True):
        img = joystick_controller._me.get_frame_read().frame
        img = cv2.resize(img, (360,240))
        frame = cv2.imencode('.jpg',img)[1].tobytes()
        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n')
        sleep(0.1)

@app.route('/video_feed')
def video_feed():
    return Response(stream(),mimetype='multipart/x-mixed-replace; boundary=frame')

joystick_controller.start()
t1 = Thread(target=stream)
t1.setDaemon(True)
t1.start()

if __name__ == '__main__':
    app.run(host="192.168.1.200", port=5000)
    