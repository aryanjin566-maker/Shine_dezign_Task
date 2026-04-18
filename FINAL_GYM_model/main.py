import os
import cv2
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware # Add this import!
import tempfile
import urllib.request
import collections
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

# --- IMPORT YOUR GEMINI MODULE ---
# This pulls the function directly from your gemini_api.py file!
from gemini_api import analyze_video

# ==========================================
# 1. SETUP & CONFIGURATION
# ==========================================
app = FastAPI(title="Gym AI Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all websites to connect (good for local testing)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# MediaPipe Model Setup
MODEL_PATH = 'pose_landmarker_heavy.task'
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_heavy/float16/1/pose_landmarker_heavy.task"

def ensure_model_exists():
    if not os.path.exists(MODEL_PATH):
        print("Downloading MediaPipe model (~20MB)...")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        print("Download complete!")

# ==========================================
# 2. DYNAMIC MEDIAPIPE TRACKER 
# ==========================================
class PatternRepCounter:
    def __init__(self):
        self.history = collections.deque(maxlen=30) 
        self.active_landmark_idx = None
        self.state = None
        self.reps = 0
        self.min_y = float('inf')  
        self.max_y = float('-inf') 

    def update_and_count(self, landmarks):
        y_coords = np.array([lm.y for lm in landmarks])

        # Find the most active joint
        if self.active_landmark_idx is None:
            self.history.append(y_coords)
            if len(self.history) == self.history.maxlen:
                variances = np.var(self.history, axis=0)
                variances[0:11] = 0 # Ignore face
                self.active_landmark_idx = np.argmax(variances)
            return self.reps

        # Track the joint and count cycles
        current_y = y_coords[self.active_landmark_idx]
        self.min_y = min(self.min_y, current_y)
        self.max_y = max(self.max_y, current_y)
        range_of_motion = self.max_y - self.min_y

        if range_of_motion < 0.05: 
            return self.reps

        upper_zone = self.min_y + (range_of_motion * 0.20)
        lower_zone = self.max_y - (range_of_motion * 0.20)

        if current_y > lower_zone and self.state != "bottom":
            self.state = "bottom"
        elif current_y < upper_zone and self.state == "bottom":
            self.state = "top"
            self.reps += 1

        return self.reps

def count_reps_dynamically(video_path: str):
    ensure_model_exists()
    tracker = PatternRepCounter()
    
    base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
    options = vision.PoseLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.VIDEO
    )
    
    final_reps = 0
    with vision.PoseLandmarker.create_from_options(options) as landmarker:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0: fps = 30
        frame_index = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
                
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
            timestamp_ms = int((frame_index / fps) * 1000)
            
            try:
                result = landmarker.detect_for_video(mp_image, timestamp_ms)
                if result.pose_landmarks:
                    final_reps = tracker.update_and_count(result.pose_landmarks[0])
            except Exception:
                pass
            
            frame_index += 1
        cap.release()
        
    return final_reps

# ==========================================
# 3. FASTAPI ENDPOINT
# ==========================================
@app.post("/analyze-workout/")
async def analyze_workout(video: UploadFile = File(...)):
    print(f"\n--- Processing Uploaded Video: {video.filename} ---")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(await video.read())
        temp_video_path = temp_video.name

    try:
        # Step 1: Call your gemini_api.py file directly!
        print("Calling gemini_api.py for analysis...")
        gemini_data = analyze_video(temp_video_path)
        
        # If Gemini fails, gemini_data will be None. We handle that gracefully.
        if not gemini_data:
            gemini_data = {"exercise": "Unknown", "using_weights": False}
            
        exercise_name = gemini_data.get("exercise", "Unknown")
        using_weights = gemini_data.get("using_weights", False)
        
        # Step 2: Use MediaPipe Pattern Tracker
        print(f"Tracking reps dynamically for: {exercise_name}")
        total_reps = count_reps_dynamically(temp_video_path)
        
        # Step 3: Return the response
        return JSONResponse(content={
            "status": "success",
            "data": {
                "exercise_identified": exercise_name,
                "weights_used": using_weights,
                "total_reps": total_reps
            }
        })
        
    finally:
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)
            print("Temporary file cleaned up.")