import cv2
import os
import time
from dotenv import load_dotenv
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.http import HttpResponse

# Load environment variables from .env file
load_dotenv()

# List of video URLs from environment variables
video_urls = [
    r"D:\Study\Internship\DjangoStreamVideo\video_streaming\video.mp4",
    os.getenv('RTSP_URL_1'),
    os.getenv('RTSP_URL_2')
]

# A dictionary to hold the capture objects for each URL
capture_dict = {}

def init_captures():
    for idx, url in enumerate(video_urls):
        if url:  # Ensure the URL is not None
            capture_dict[str(idx)] = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
            capture_dict[str(idx)].set(cv2.CAP_PROP_BUFFERSIZE, 2)

def gen_frames(capture, url):
    retry_delay = 0.5  # Delay in seconds before retrying to reconnect
    while True:
        success, frame = capture.read()
        if not success:
            print(f"Reconnecting to {url}")
            capture.release()
            time.sleep(retry_delay)
            capture.open(url)
            continue
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.03)  # Adding a short sleep interval to smoothen the stream

def stream_video(request, url_id):
    url = video_urls[int(url_id)]
    if url_id not in capture_dict:
        return HttpResponse("Invalid stream ID")

    capture = capture_dict[url_id]
    return StreamingHttpResponse(gen_frames(capture, url),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

def index(request):
    return render(request, 'stream/index.html', {'urls': video_urls})

# Initialize capture objects on startup
init_captures()
