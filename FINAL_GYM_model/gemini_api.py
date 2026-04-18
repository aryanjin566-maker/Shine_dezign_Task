import google.generativeai as genai
import time
import json
import os

# --- CONFIGURE YOUR KEY HERE ---
genai.configure(api_key="")

def get_safe_model_name():
    """Finds the correct Flash model dynamically to avoid version errors."""
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods and 'flash' in m.name:
                return m.name 
    except Exception:
        pass
    return "gemini-1.5-flash-latest"

def analyze_video(video_path: str):
    """Phase 1: Uploads video, gets exercise type, and returns a dictionary."""
    if not os.path.exists(video_path):
        print(f"[Error] Video file not found at: {video_path}")
        return None

    print("[Phase 1] Uploading video to Gemini...")
    try:
        video_file = genai.upload_file(path=video_path)
        
        print("[Phase 1] Waiting for Google servers to process the video", end="")
        while video_file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(2)
            video_file = genai.get_file(video_file.name)
        print("\n[Phase 1] Processing complete!")
            
        model_name = get_safe_model_name()
        model = genai.GenerativeModel(model_name=model_name)
        
        prompt = """
        Watch this exercise video carefully. Identify the specific gym exercise being performed.
        Return ONLY a JSON object with exactly these two keys:
        {
          "exercise": "Name of Exercise",
          "using_weights": true/false
        }
        """
        
        print(f"[Phase 1] Asking {model_name} to identify the exercise...")
        response = model.generate_content([video_file, prompt])
        
        # Clean up
        genai.delete_file(video_file.name)
      
        raw_text = response.text.replace('```json', '').replace('```', '').strip()
        result = json.loads(raw_text)
        print(f"[Phase 1] Gemini Result: {result}")
        return result
        
    except Exception as e:
        print(f"[Phase 1 Error]: {e}")
        return {"exercise": "Unknown", "using_weights": False}

# --- TEST THIS FILE INDEPENDENTLY ---
if __name__ == "__main__":
    # Change this to a real video path on your computer to test
    test_video = r"C:\Users\ashna\Desktop\FINAL_GYM_model\barbell biceps curl_1.mp4"
    print("--- Testing Phase 1 Independently ---")
    analyze_video(test_video)
