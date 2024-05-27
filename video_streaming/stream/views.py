
# Create your views here.
import cv2
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.http import HttpResponse
import threading

# Global variables for capturing video
cap_mp4 = cv2.VideoCapture(r'D:\Study\Internship\DjangoStreamVideo\video_streaming\video.mp4')
cap_rtsp1 = cv2.VideoCapture('rtsp://admin:12345@192.168.1.210:554/Streaming/Channels/101')
cap_rtsp2 = cv2.VideoCapture('rtsp://170.93.143.139/rtplive/470011e600ef003a004ee33696235daa')

def gen_frames(capture):
    while True:
        success, frame = capture.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def stream_video(request, stream_id):
    if stream_id == '1':
        capture = cap_mp4
    elif stream_id == '2':
        capture = cap_rtsp1
    elif stream_id == '3':
        capture = cap_rtsp2
    else:
        return HttpResponse("Invalid stream ID")

    return StreamingHttpResponse(gen_frames(capture),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

def index(request):
    return render(request, 'stream/index.html')
