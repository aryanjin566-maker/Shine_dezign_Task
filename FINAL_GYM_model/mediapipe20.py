import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import urllib.request
import os
import collections

# --- MODEL SETUP ---
MODEL_PATH = 'pose_landmarker_heavy.task'
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_heavy/float16/1/pose_landmarker_heavy.task"

def ensure_model_exists():
    """Downloads the required MediaPipe model file if it doesn't exist."""
    if not os.path.exists(MODEL_PATH):
        print(f"[Phase 2] Downloading modern MediaPipe model (~20MB)...")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        print("[Phase 2] Download complete!")

# --- DYNAMIC PATTERN TRACKER ---
class PatternRepCounter:
    def __init__(self):
        # Store the Y-coordinates of the first 30 frames to find what is moving
        self.history = collections.deque(maxlen=30) 
        self.active_landmark_idx = None
        
        # Tracking the actual movement cycle
        self.state = None
        self.reps = 0
        self.min_y = float('inf')  # Highest point in the screen (Y is 0 at top)
        self.max_y = float('-inf') # Lowest point in the screen

    def update_and_count(self, landmarks):
        # Extract the Y coordinate (vertical movement) of all 33 landmarks
        y_coords = np.array([lm.y for lm in landmarks])

        # Step 1: Observation Phase - Figure out which body part is moving most
        if self.active_landmark_idx is None:
            self.history.append(y_coords)
            
            # Once we have enough frames, calculate the variance (movement)
            if len(self.history) == self.history.maxlen:
                variances = np.var(self.history, axis=0)
                
                # We ignore landmarks 0-10 (the face) because head bobbing isn't a rep
                variances[0:11] = 0 
                
                # Lock onto the joint with the highest movement variance
                self.active_landmark_idx = np.argmax(variances)
                print(f"\n[Phase 2 Tracker] Locked onto joint #{self.active_landmark_idx} for pattern tracking.")
            return self.reps

        # Step 2: Tracking Phase - Track only the most active joint
        current_y = y_coords[self.active_landmark_idx]

        # Dynamically update the known highest and lowest points of this joint
        self.min_y = min(self.min_y, current_y)
        self.max_y = max(self.max_y, current_y)
        range_of_motion = self.max_y - self.min_y

        # If the range of motion is tiny, they are just twitching, not doing a rep
        if range_of_motion < 0.05: 
            return self.reps

        # Step 3: Cycle Detection - Define the "top" and "bottom" zones
        # We use a 20% buffer so they don't have to perfectly hit the exact same max/min every time
        upper_zone = self.min_y + (range_of_motion * 0.20)
        lower_zone = self.max_y - (range_of_motion * 0.20)

        # Count the cycles based on changing directions
        if current_y > lower_zone and self.state != "bottom":
            self.state = "bottom"
        elif current_y < upper_zone and self.state == "bottom":
            self.state = "top"
            self.reps += 1
            print(f"[Phase 2] Pattern match! Rep Counted: {self.reps}")

        return self.reps


def process_video_and_count(video_path: str, gemini_result: dict):
    """Takes video, uses dynamic pattern recognition to count reps, returns total."""
    if not os.path.exists(video_path):
        print(f"[Error] Video file not found at: {video_path}")
        return 0

    ensure_model_exists()
    exercise_type = gemini_result.get("exercise", "Unknown").upper()
    print(f"[Phase 2] Initializing dynamic tracker for: {exercise_type}")
    
    # Initialize our new dynamic pattern counter
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
            result = landmarker.detect_for_video(mp_image, timestamp_ms)
            
            try:
                if result.pose_landmarks:
                    # Pass the landmarks to our dynamic tracker
                    landmarks = result.pose_landmarks[0]
                    final_reps = tracker.update_and_count(landmarks)
            except Exception:
                pass
            
            frame_index += 1

        cap.release()
        
    print(f"\n[Phase 2] Tracking complete. Final Count: {final_reps}")
    return final_reps

# --- TEST INDEPENDENTLY ---
if __name__ == "__main__":
    test_video = r"C:\Users\ashna\Desktop\FINAL_GYM_model\Do 100 reps of these 2 bicep exercises for BIGGER ARMS.mp4"
    fake_gemini_data = {"exercise": "Unknown Exercise", "using_weights": False}
    
    print("--- Testing Phase 2 (Dynamic Pattern Recognition) ---")
    process_video_and_count(test_video, fake_gemini_data)