from fastapi import FastAPI, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
import shutil
import uuid
import models, database
import requests
import os
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ DB Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================
# SIGNUP
# =========================
@app.post("/signup")
def signup(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user_id = str(uuid.uuid4())[:8]

    user = models.User(
        name=name,
        email=email,
        password=password,
        user_id=user_id
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User Created", "user_id": user_id}

# =========================
# LOGIN
# =========================
@app.post("/login")
def login(
    user_id: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(
        models.User.user_id == user_id,
        models.User.password == password
    ).first()

    if user:
        return {"message": "Login successful"}
    else:
        return {"message": "Invalid credentials"}

# =========================
# UPLOAD IMAGE
# =========================
@app.post("/upload")
def upload(
    user_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    os.makedirs("images", exist_ok=True)

    # ✅ Unique filename
    filename = str(uuid.uuid4()) + "_" + file.filename
    file_location = f"images/{filename}"

    # ✅ Save file
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ✅ Save path in DB
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    user.image_path = file_location
    db.commit()

    print("Saved at:", file_location)

    return {"message": "Image uploaded", "path": file_location}

# =========================
# GET RESULT
# =========================
@app.post("/get-result")
def get_result(user_id: str, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.user_id == user_id).first()

    print("Image path from DB:", user.image_path)

    # ✅ Send FORM data (match predict API)
    response = requests.post(
        "http://127.0.0.1:8001/predict",
        data={"image_path": user.image_path}
    )

    print("Model response:", response.text)

    response_data = response.json()

    if "result" not in response_data:
        return {"error": response_data}

    result = response_data["result"]
    confidence = response_data["confidence"]

    return {
        "message": f"It is a {result} image",
        "confidence": confidence
    }