from fastapi import FastAPI, Request, Form
from database import get_db

app = FastAPI()

# Simple session storage (for learning purpose)


session = {}

# ---------------- USER REGISTER ----------------
@app.post("/register")
def register(
    user_id: int = Form(...),
    name: str = Form(...),
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(...)
):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO user_info VALUES (%s,%s,%s,%s,%s)",
        (user_id, name, email, username, password)
    )
    db.commit()
    return {"message": "User registered successfully"}

# ---------------- LOGIN ----------------
@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM user_info WHERE username=%s AND password=%s",
        (username, password)
    )
    user = cursor.fetchone()

    if user:
        session["user"] = user
        return {"message": "Login successful"}
    return {"error": "Invalid credentials"}

# ---------------- CREATE POST ----------------
@app.post("/create_post")
def create_post(caption: str = Form(...)):
    if "user" not in session:
        return {"error": "Login required"}
    
    print(session)
    user_id = session["user"]["user_id"]


    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO post (user_id, caption) VALUES (%s, %s)",
        (user_id, caption)
    )
    db.commit()
    return {"message": "Post created successfully"}

# ---------------- LIKE POST ----------------
@app.post("/like_post")
def like_post(post_id: int = Form(...)):
    if "user" not in session:
        return {"error": "Login required"}

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO liked (post_id, user_id) VALUES (%s,%s)",
        (post_id, session["user"]["user_id"])
    )
    db.commit()
    return {"message": "Post liked"}

# ---------------- COMMENT POST ----------------
@app.post("/comment")
def comment(post_id: int = Form(...), text: str = Form(...)):
    if "user" not in session:
        return {"error": "Login required"}

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO comment (post_id, user_id, comment_text) VALUES (%s,%s,%s)",
        (post_id, session["user"]["user_id"], text)
    )
    db.commit()
    return {"message": "Comment added"}

# ---------------- VIEW WHO LIKED POST ----------------
@app.get("/post_likes")
def view_likes(post_id: int = Form(...)):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT user_info.user_id, user_info.username
        FROM liked
        JOIN user_info ON liked.user_id = user_info.user_id
        WHERE liked.post_id = %s
    """, (post_id,))

    return cursor.fetchall()

# ---------------- UPDATE PROFILE ----------------
@app.put("/update_profile")
def update_profile(
    name: str = Form(...),
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(...)
):
    if "user" not in session:
        return {"error": "Login required"}

    user_id = session["user"]["user_id"]

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE user_info
        SET name=%s, email=%s, username=%s, password=%s
        WHERE user_id=%s
    """, (name, email, username, password, user_id))

    db.commit()

    # update session data also
    session["user"]["name"] = name
    session["user"]["email"] = email
    session["user"]["username"] = username
    session["user"]["password"] = password

    return {"message": "Profile updated successfully"}


# ---------------- DELETE PROFILE ----------------
@app.delete("/delete_profile")
def delete_profile():
    if "user" not in session:
        return {"error": "Login required"}

    user_id = session["user"]["user_id"]

    db = get_db()
    cursor = db.cursor()

    # delete comments
    cursor.execute("DELETE FROM comment WHERE user_id=%s", (user_id,))

    # delete likes
    cursor.execute("DELETE FROM liked WHERE user_id=%s", (user_id,))

    # delete posts
    cursor.execute("DELETE FROM post WHERE user_id=%s", (user_id,))

    # delete user profile
    cursor.execute("DELETE FROM user_info WHERE user_id=%s", (user_id,))

    db.commit()
    session.clear()

    return {"message": "Profile deleted successfully"}

# ---------------- LOGOUT ----------------
@app.get("/logout")
def logout():
    session.clear()
    return {"message": "Logged out successfully"}
