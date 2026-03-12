from fastapi import FastAPI, Depends, HTTPException, status, Form
from fastapi.middleware.cors import CORSMiddleware  # Added for CORS
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError  # For DB errors
from models import Base, User
from werkzeug.security import generate_password_hash, check_password_hash
from jose import JWTError, jwt
from datetime import datetime, timedelta
import re  # For email validation

# Database setup
DATABASE_URL = "mysql+mysqlconnector://root:1234@localhost:3306/bank_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# JWT setup
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (restrict in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def validate_email(email: str) -> bool:
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

@app.get("/")
def root():
    return {"message": "Welcome to the Bank Management System API. Visit /docs for API documentation or /register for info."}

@app.get("/register")  # Added for browser testing (shows info, not form)
def register_info():
    return {"message": "Use POST to register. Required: user_id, password, name, email. Visit /docs to test."}

@app.post("/register")
def register(user_id: str = Form(...), password: str = Form(...), name: str = Form(...), email: str = Form(...), db: Session = Depends(get_db)):
    if not validate_email(email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    try:
        if db.query(User).filter((User.user_id == user_id) | (User.email == email)).first():
            raise HTTPException(status_code=400, detail="User ID or email already exists")
        hashed_password = generate_password_hash(password)
        user = User(user_id=user_id, password_hash=hashed_password, name=name, email=email)
        db.add(user)
        db.commit()
        return {"message": "Profile created successfully"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Registration failed due to database error")

@app.post("/login")
def login(user_id: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user or not check_password_hash(user.password_hash, password):
        raise HTTPException(status_code=401, detail="Invalid user ID or password")
    token = create_access_token({"sub": user_id})
    return {"message": "Login successful", "access_token": token, "token_type": "bearer"}

@app.get("/profile")
def get_profile(user_id: str = Depends(verify_token), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    return {"user_id": user.user_id, "name": user.name, "email": user.email}

@app.put("/profile")
def update_profile(name: str = Form(...), email: str = Form(...), user_id: str = Depends(verify_token), db: Session = Depends(get_db)):
    if not validate_email(email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    user = db.query(User).filter(User.user_id == user_id).first()
    user.name = name
    user.email = email
    db.commit()
    return {"message": "Profile updated successfully"}

@app.delete("/profile")
def delete_profile(user_id: str = Depends(verify_token), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    db.delete(user)
    db.commit()
    return {"message": "Profile deleted successfully"}

@app.post("/credit")
def credit(amount: float = Form(...), user_id: str = Depends(verify_token), db: Session = Depends(get_db)):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    user = db.query(User).filter(User.user_id == user_id).first()
    user.balance += amount
    db.commit()
    return {"message": "Amount credited successfully", "balance": user.balance}

@app.post("/debit")
def debit(amount: float = Form(...), user_id: str = Depends(verify_token), db: Session = Depends(get_db)):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    user = db.query(User).filter(User.user_id == user_id).first()
    if user.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    user.balance -= amount
    db.commit()
    return {"message": "Amount debited successfully", "balance": user.balance}

@app.get("/balance")
def get_balance(user_id: str = Depends(verify_token), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    return {"balance": user.balance}