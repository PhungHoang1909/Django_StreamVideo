from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from .models import *  
from django.core.mail import EmailMessage  
from django.views.decorators import gzip  
import cv2  
import threading  

@gzip.gzip_page
def Home(request):
    try:
        cam = VideoCamera()
        # Return a streaming HTTP response using the gen generator function
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except Exception as e:
        print(f"Error: {e}") 
        pass  
    return render(request, 'base.html')

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        if not self.video.isOpened():
            raise Exception("Could not open video device")
        # Read the first frame from the video capture
        (self.grabbed, self.frame) = self.video.read()
        if not self.grabbed:
            raise Exception("Could not read frame from video device")
        threading.Thread(target=self.update, args=()).start()
        # Load the pre-trained Haar Cascade classifier for face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        # Get the current frame
        image = self.frame

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Encode the frame as JPEG
        _, jpeg = cv2.imencode('.jpg', image)

        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()
            if not self.grabbed:
                break

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
