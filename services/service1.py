from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.capture_screenshot import capture_screenshot
from src.config_reader import get_rtsp_url
import os
import cv2
import numpy as np
from datetime import datetime
import re
import time

router = APIRouter()

# Get the base directory of the current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Move up one level (from services to PWANI_CAMERA_INTEGRATION)
PROJECT_ROOT = os.path.dirname(BASE_DIR)

# Now define the image save directory directly
SAVE_DIR = os.path.join(PROJECT_ROOT, "images")
os.makedirs(SAVE_DIR, exist_ok=True)

class ScreenshotRequest(BaseModel):
    stage: str
    view: str
    status: str

@router.post("")
def screenshot(request: ScreenshotRequest):
    t0 = time.time()

    if request.stage in ["WB2", "WB1", "main_gate", "offloading"]:
        print(f"🚚 The truck is {request.status} {request.stage}, requesting {request.view} view.")
    else:
        print(f"🚚 The truck is at the main gate, requesting view. Providing main gate view.")

    try:
        rtsp_url, focus = get_rtsp_url(request.stage, request.status, request.view)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    match = re.findall(r'\d+', focus)
    x1, x2, y1, y2 = map(int, match)

    print(f"RTSP URL: {rtsp_url}")

    frame = capture_screenshot(rtsp_url)
    t1 = time.time()

    frame = frame[x1:x2, y1:y2]

    if frame is None or frame.size == 0:
        raise HTTPException(status_code=500, detail="Failed to capture frame. RTSP stream might be down.")

    if isinstance(frame, bytes):
        frame = np.frombuffer(frame, dtype=np.uint8)
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    t2 = time.time()

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    if request.stage in ["WB2", "WB1", "main_gate"]:
        filename = f"{request.stage}_{request.status}_truck_{request.view}_{now}.webp"
    else:
        filename = f"main_gate_truck_{now}.webp"
        
    print(PROJECT_ROOT)

    # Construct full absolute file path
    filepath = os.path.join(SAVE_DIR, filename)

    print("Saved to", filepath)

    ok = cv2.imwrite(filepath, frame, [cv2.IMWRITE_WEBP_QUALITY, 20])
    if not ok:
        raise HTTPException(status_code=500, detail=f"Could not save image to {filepath}")

    t3 = time.time()

    print(
        f"[Timing] capture: {t1 - t0:.2f}s, "
        f"decode: {t2 - t1:.2f}s, "
        f"save: {t3 - t2:.2f}s → total: {t3 - t0:.2f}s"
    )

    # Relative path for response
    img_rel_path = os.path.join("camera", "PWANI_CAMERA_INTEGRATION", "images", filename)
    return {"img_path": img_rel_path}
