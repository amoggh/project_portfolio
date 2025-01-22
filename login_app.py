from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo

app = Flask(__name__)

# Secret key for session (used for flash messages)
app.secret_key = 'supersecretkey'

# MongoDB Configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/portifyDB"
mongo = PyMongo(app)

# ---------- ROUTES ----------

# Home Page (redirect to login for now)
@app.route('/')
def home():
    return redirect(url_for('login'))

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = mongo.db.users.find_one({'username': username})
        
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            flash('Welcome back! You have successfully logged in.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
            return redirect(url_for('login'))
    
    return render_template('/login.html')

# Sign-up Page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = mongo.db.users.find_one({'username': username})
        existing_email = mongo.db.users.find_one({'email': email})
        
        if existing_user:
            flash('This username is already taken. Please choose another one.', 'error')
            return redirect(url_for('signup'))
        
        if existing_email:
            flash('An account with this email already exists. Please login instead.', 'error')
            return redirect(url_for('signup'))
        
        hashed_password = generate_password_hash(password)
        
        mongo.db.users.insert_one({
            'username': username,
            'email': email,
            'password': hashed_password
        })
        
        flash('Your account has been created successfully! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('/signup.html')

# Dashboard (After successful login)
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return f"<h1>Welcome, {session['username']}!</h1><a href='/logout'>Logout</a>"
    else:
        flash('You need to log in first.', 'error')
        return redirect(url_for('login'))

# Logout Route
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# Examples of using flash messages in your routes:

# For success messages
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if user_authenticated:
            flash('Successfully logged in!', 'success')
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

# For signup success
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if user_created:
            flash('Account created successfully! Please log in.', 'success')
        elif username_exists:
            flash('Username already exists. Please choose another.', 'error')
        elif email_exists:
            flash('Email already registered. Please login instead.', 'error')
    return render_template('signup.html')

# You can also use warning and info categories
flash('Please verify your email address.', 'warning')
flash('Maintenance scheduled for tomorrow.', 'info')

if __name__ == '__main__':
    app.run(debug=True)