import configparser
import threading
import time
import cv2
import mysql.connector
from fastapi import APIRouter, Response
from starlette.responses import StreamingResponse

router = APIRouter()

# Load database config
config = configparser.ConfigParser()
config.read("config/config.ini")

DB_HOST = config["database"]["DB_HOST"]
DB_NAME = config["database"]["DB_NAME"]
DB_USER = config["database"]["DB_USER"]
DB_PASSWORD = config["database"]["DB_PASSWORD"]
DB_TABLE = config["database"]["DB_TABLE"]

camera_streams = {}  # {cameraId: {'link': rtspLink, 'stop': Event}}

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def fetch_cameras():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, rtspLink FROM {DB_TABLE}")
    cameras = cursor.fetchall()
    cursor.close()
    conn.close()
    return {str(cam_id): link for cam_id, link in cameras}

def generate_frames(rtsp_link: str, stop_event: threading.Event):
    rtsp_link = rtsp_link[:-1] + '2'  # Modify last char (as in original code)
    cap = cv2.VideoCapture(rtsp_link)

    while not stop_event.is_set():
        success, frame = cap.read()
        if not success:
            break
        encode_param = [int(cv2.IMWRITE_WEBP_QUALITY), 20]
        _, buffer = cv2.imencode('.webp', frame, encode_param)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/webp\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

def start_stream(camera_id: str, rtsp_link: str):
    stop_event = threading.Event()
    camera_streams[camera_id] = {
        'link': rtsp_link,
        'stop': stop_event
    }

def update_camera_streams():
    while True:
        new_cameras = fetch_cameras()
        current_ids = set(camera_streams.keys())
        new_ids = set(new_cameras.keys())

        # Add new cameras
        for cam_id in new_ids - current_ids:
            print(f"[INFO] New camera detected: {cam_id}")
            start_stream(cam_id, new_cameras[cam_id])

        # Remove deleted cameras
        for cam_id in current_ids - new_ids:
            print(f"[INFO] Camera removed: {cam_id}")
            camera_streams[cam_id]['stop'].set()
            del camera_streams[cam_id]

        # Update RTSP link if changed
        for cam_id in new_ids & current_ids:
            old_link = camera_streams[cam_id]['link']
            new_link = new_cameras[cam_id]
            if old_link != new_link:
                print(f"[INFO] RTSP updated for {cam_id}")
                camera_streams[cam_id]['stop'].set()
                del camera_streams[cam_id]
                start_stream(cam_id, new_link)

        time.sleep(5)

# Start background thread on module import
threading.Thread(target=update_camera_streams, daemon=True).start()

@router.get("/stream/camera{camera_id}")
def stream_camera(camera_id: str):
    if camera_id in camera_streams:
        return StreamingResponse(generate_frames(camera_streams[camera_id]['link'], camera_streams[camera_id]['stop']),
                                 media_type="multipart/x-mixed-replace; boundary=frame")
    else:
        return Response(content=f"Camera {camera_id} not found.", status_code=404)