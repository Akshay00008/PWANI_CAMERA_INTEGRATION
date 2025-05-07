import cv2
import numpy as np

def capture_screenshot(rtsp_url):
    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        print("Error: Unable to open RTSP stream")
        return None

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Error: Failed to capture frame")
        return None

    return frame  # This should be a NumPy array