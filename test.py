import cv2
import imutils
from imutils.video import VideoStream
rtsp_url = "rtsp://rtspstream:61101fa39bb5a8c8b0994797aade10e7@zephyr.rtsp.stream/movie"
video_stream = VideoStream(rtsp_url).start()

while True:
    frame = video_stream.read()
    if frame is None:
        continue

    frame = imutils.resize(frame,width=400)
    cv2.imshow('AsimCodeCam', frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cv2.destroyAllWindows()
video_stream.stop()