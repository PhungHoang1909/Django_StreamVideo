import cv2
import os
import time
from dotenv import load_dotenv
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.http import HttpResponse
import threading

# Load environment variables from .env file
load_dotenv()

# List of video URLs from environment variables
video_urls = [
    r"D:\Study\Internship\DjangoStreamVideo\video_streaming\video.mp4",
    os.getenv('RTSP_URL_1'),
    os.getenv('RTSP_URL_2'),
    # os.getenv('RTSP_URL_3'),
]

# A dictionary to hold the capture objects for each URL
capture_dict = {}

# Capture each RTSP URLs and config: Size, FPS, buffersize
def init_captures():
    for idx, url in enumerate(video_urls):
        if url:  
            capture = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
            capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)
            capture.set(cv2.CAP_PROP_FPS, 30)  # Set frame rate to 30 FPS
            capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            capture_dict[str(idx)] = capture

# Read frame and convert it to jpeg and yield each frame to browser
def gen_frames(capture, url):
    retry_delay = 0.5  
    while True:
        success, frame = capture.read()
        if not success:
            print(f"Reconnecting to {url}")
            capture.release()
            time.sleep(retry_delay)
            capture.open(url)
            continue
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.03)  

# Stream video to browser
def stream_video(request, url_id):
    url = video_urls[int(url_id)]
    if url_id not in capture_dict:
        return HttpResponse("Invalid stream ID")

    capture = capture_dict[url_id]
    return StreamingHttpResponse(gen_frames(capture, url),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

def index(request):
    return render(request, 'stream/index.html', {'urls': video_urls})

init_captures() # Khởi tạo các đối tượng capture ngay khi module được load.
