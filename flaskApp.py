import cv2
from flask import Flask, render_template, Response, stream_with_context, request
from time import sleep
from joystickController import JoystickController
from threading import Thread, Event
import numpy as np
import mediapipe as mp

shared_bool = Event()
joystick_controller = JoystickController(shared_bool)


app = Flask('__name__')

w, h = 360, 240
fbRange = [6200, 6800]
pid = [0.4, 0.4, 0]
pError = 0

minDetectionConf = 0.5
mpFaceDetection = mp.solutions.face_detection
mpDraw = mp.solutions.drawing_utils
faceDetection = mpFaceDetection.FaceDetection()

def findFace(img):
    myFaceListC = []
    myFaceListArea = []

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceDetection.process(imgRGB)
    bboxs = []  
    if results.detections:
        for id,detection in enumerate(results.detections):
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, ic = img.shape
            bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                    int(bboxC.width * iw), int(bboxC.height * ih)
            
            bboxs.append([id, bbox, detection.score]) 
            img = fancyDraw(img, bbox)
            cv2.putText(img, f'{int(detection.score[0]*100)}%',\
                    (bbox[0],bbox[1]-20),cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
            x, y, w, h = bbox
            cx = x + w//2
            cy = y + h//2
            area = w * h
            myFaceListC.append([cx,cy])
            myFaceListArea.append(area)
        if len(myFaceListArea) != 0:
            i = myFaceListArea.index(max(myFaceListArea))
            return img, [myFaceListC[i], myFaceListArea[i]]
        else:
            return img, [[0, 0], 0]

def fancyDraw(img,bbox, l=30, t=5, rt=1):
    x, y, w, h = bbox
    x1, y1 = x+w, y+h

    cv2.rectangle(img,bbox,(255, 0, 255), rt)
    # Top Left x,y
    cv2.line(img, (x,y), (x+l,y), (255,0,255), t)
    cv2.line(img, (x,y), (x,y+l), (255,0,255), t)

    # Top Right x,y
    cv2.line(img, (x1,y), (x1-l,y), (255,0,255), t)
    cv2.line(img, (x1,y), (x1,y+l), (255,0,255), t)
    # Bottom Left x,y
    cv2.line(img, (x,y1), (x+l,y1), (255,0,255), t)
    cv2.line(img, (x,y1), (x,y1-l), (255,0,255), t)

    # Bottom Right x,y
    cv2.line(img, (x1,y1), (x1-l,y1), (255,0,255), t)
    cv2.line(img, (x1,y1), (x1,y1-l), (255,0,255), t)

    return img

def trackFace(info, w, pid, pError,track=False):
    if(track):
        area = info[1]
        x,y = info[0]
        error = x - w//2
        speed = pid[0]* error + pid[1]*(error-pError)
        speed = int(np.clip(speed,-100,100))
        fb = 0

        if area > fbRange[0] and area < fbRange[1]:
            fb = 0
        elif area> fbRange[1]:
            fb=-20
        elif area < fbRange[0] and area != 0:
            fb = 20

        if x == 0:
            speed = 0
            error = 0

        joystick_controller._me.send_rc_control(0, fb, 0, speed)
        return error


@app.route('/')
def index():
    return render_template('index.html')

def stream(shared_bool:Event):
    while(True):
        img = joystick_controller._me.get_frame_read().frame
        img = cv2.resize(img, (w,h))
        try:
            img, info = findFace(img)
        except:
            info =[[0, 0], 0]
        if(shared_bool.is_set()):    
            pError = trackFace(info,w,pid,pError,shared_bool.is_set())
        frame = cv2.imencode('.jpg',img)[1].tobytes()
        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n')
        sleep(0.1)

@app.route('/video_feed')
def video_feed():
    return Response(stream(shared_bool),mimetype='multipart/x-mixed-replace; boundary=frame')

joystick_controller.start()
t1 = Thread(target=stream, args=(shared_bool,))
t1.start()

if __name__ == '__main__':
    app.run(host="192.168.0.150", port=5000)
    