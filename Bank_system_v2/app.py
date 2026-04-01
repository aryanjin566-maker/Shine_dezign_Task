from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
import mysql.connector
import os
import random
import string
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a secure key
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')  # Absolute path
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',  # Replace with your MySQL username
        password='1234',  # Replace with your MySQL password
        database='bank_system'
    )

# Function to generate unique account number
def generate_account_number():
    conn = get_db_connection()
    cursor = conn.cursor()

    while True:
        account_number = ''.join(random.choices(string.digits, k=10))

        cursor.execute(
            "SELECT 1 FROM users WHERE account_number = %s LIMIT 1",
            (account_number,)
        )

        if cursor.fetchone() is None:
            cursor.close()
            conn.close()
            return account_number

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        address = request.form['address']
        password = request.form['password']
        image = request.files['image']
        
        # Validate image
        if image and image.filename != '':
            if not image.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                flash('Invalid image file. Only PNG, JPG, JPEG, GIF allowed.', 'danger')
                return redirect(request.url)
            if image.content_length > 2 * 1024 * 1024:  # 2MB limit
                flash('Image file too large. Max 2MB.', 'danger')
                return redirect(request.url)
        
        account_number = generate_account_number()
        image_filename = None
        if image and image.filename != '':
            safe_filename = secure_filename(image.filename)
            image_filename = f"{account_number}_{safe_filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image.save(file_path)
            print(f"DEBUG: Image saved to: {file_path}")
            print(f"DEBUG: File exists after save: {os.path.exists(file_path)}")
            print(f"DEBUG: Image filename for DB: {image_filename}")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO users (user_id, password, name, phone_number, email, address, account_number, image, balance) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 0.00)
            """, (account_number, password, name, phone_number, email, address, account_number, image_filename))
            conn.commit()
            print(f"DEBUG: User registered with image: {image_filename}")
            session['new_account_number'] = account_number
            return redirect(url_for('registration_success'))
        except mysql.connector.IntegrityError:
            flash('Account number generation failed, please try again.', 'danger')
        finally:
            cursor.close()
            conn.close()
    return render_template('register.html')

# Registration Success page
@app.route('/registration_success')
def registration_success():
    account_number = session.pop('new_account_number', None)
    if not account_number:
        return redirect(url_for('home'))
    return render_template('registration_success.html', account_number=account_number)

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']  # This is the account_number
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE account_number = %s AND password = %s", (user_id, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            session['user_id'] = user['account_number']
            flash('Login successful', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid user ID or password', 'danger')
    return render_template('login.html')

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE account_number = %s", (session['user_id'],))
    user = cursor.fetchone() #user variable is store the row of the account number . detail in the row is like person name , id , phone number etc. . this store dictionary 
    cursor.close()
    conn.close() 
    print(f"DEBUG: Dashboard user image: {user['image']}")
    return render_template('dashboard.html', user=user) # here user = user pass the user information 

# Serve uploaded images
@app.route('/uploads/<filename>')
def uploaded_file(filename):    
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except FileNotFoundError:
        print(f"DEBUG: File not found: {filename}")
        return "File not found", 404

# Credit amount
@app.route('/credit', methods=['GET', 'POST'])
def credit():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if  request.method == 'POST':
        amount = float(request.form['amount'])
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET balance = balance + %s WHERE account_number = %s", (amount, session['user_id']))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Amount credited successfully', 'success')
        return redirect(url_for('dashboard'))
    return render_template('credit.html')

# Debit amount
@app.route('/debit', methods=['GET', 'POST'])
def debit():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        amount = float(request.form['amount'])
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT balance FROM users WHERE account_number = %s", (session['user_id'],))
        user = cursor.fetchone()
        if user['balance'] >= amount:
            cursor.execute("UPDATE users SET balance = balance - %s WHERE account_number = %s", (amount, session['user_id']))
            conn.commit()
            flash('Amount debited successfully', 'success')
        else:
            flash('Insufficient balance', 'danger')
        cursor.close()
        conn.close()
        return redirect(url_for('dashboard'))
    return render_template('debit.html')

# View balance
@app.route('/balance')
def balance():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT balance FROM users WHERE account_number = %s", (session['user_id'],))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('balance.html', user=user)

# Update profile
@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        address = request.form['address']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET name = %s, phone_number = %s, email = %s, address = %s WHERE account_number = %s", (name, phone_number, email, address, session['user_id']))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('dashboard'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE account_number = %s", (session['user_id'],))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('update_profile.html', user=user)

# Delete profile
@app.route('/delete_profile', methods=['POST'])
def delete_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT image FROM users WHERE account_number = %s", (session['user_id'],))
        user = cursor.fetchone()
        image_filename = user['image'] if user else None
        
        cursor.execute("DELETE FROM users WHERE account_number = %s", (session['user_id'],))
        conn.commit()
        cursor.close()
        conn.close()
        
        if image_filename and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], image_filename)):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
        
        session.pop('user_id', None)
        flash('Profile deleted successfully', 'success')
        return redirect(url_for('home'))
    except Exception as e:
        flash(f'Error deleting profile: {str(e)}', 'danger')
        return redirect(url_for('dashboard'))

# Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logout successful', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
