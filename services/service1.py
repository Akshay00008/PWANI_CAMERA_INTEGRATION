from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.capture_screenshot import capture_screenshot
from src.shorten_rtsp import get_last_part
from src.config_reader import get_rtsp_url
import os
import cv2
import numpy as np
from datetime import datetime

router = APIRouter()

SAVE_DIR = os.path.join(os.getcwd(), 'images')
os.makedirs(SAVE_DIR, exist_ok=True)

class ScreenshotRequest(BaseModel):
    stage: str
    view: str
    status: str

@router.post("")
def screenshot(request: ScreenshotRequest):
    if request.stage == "WB2":
        print(f"🚚 The truck is {request.status} {request.stage}, requesting {request.view} view.")
    else:
        print(f"🚚 The truck is at the {request.stage}, requesting view.")

    try:
        rtsp_url = get_rtsp_url(request.stage, request.status, request.view)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    print(f"RTSP URL: {rtsp_url}")

    # shorten_rtsp = get_last_part(rtsp_url)

    frame = capture_screenshot(rtsp_url)

    if frame is None or frame.size == 0:
        raise HTTPException(status_code=500, detail="Failed to capture frame. RTSP stream might be down.")

    if isinstance(frame, bytes):
        frame = np.frombuffer(frame, dtype=np.uint8)
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    if request.stage == "WB2":
        filename = f"{request.stage}_{request.status}_truck_{request.view}_{now}.png" 
    else:
        filename = f"{request.stage}_truck_{now}.png" 

    filepath = os.path.join("/apps/camera/PWANI_CAMERA_INTEGRATION/images$", filename)
    
    cv2.imwrite(filepath, frame)

    return {"img_path": filepath}