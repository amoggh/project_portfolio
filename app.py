import os
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)
app.run(debug=True)

# MongoDB Configuration
try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['portfolio_generator']
    collection = db['user_portfolios']
    print("✅ Connected to MongoDB")
except Exception as e:
    print(f"❌ Error connecting to MongoDB: {e}")

# Directory to store uploaded resumes
UPLOAD_FOLDER = 'uploads/resume'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to render the form
@app.route('/')
def index():
    return render_template("index.html")  # Fixed template path

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    try:
        print("Form submitted")  # Debugging output

        # Get form data and file
        resume_file = request.files.get('resume')
        name = request.form.get('name')
        email = request.form.get('email')
        education = request.form.get('education')
        bio = request.form.get('bio')
        job = request.form.get('job')
        projects = request.form.get('projects')
        passions = request.form.get('passions')
        future_goals = request.form.get('futureGoals')
        social_links = request.form.get('socialLinks')
        resume_filename = None

        # Validate required fields
        if not name or not email:
            raise ValueError("Name and Email are required.")

        # Check and save resume file if provided
        if resume_file and allowed_file(resume_file.filename):
            filename = secure_filename(resume_file.filename)
            resume_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            resume_file.save(resume_path)
            resume_filename = filename
            print(f"Resume saved at {resume_path}")  # Debugging output


        # Insert all form data into MongoDB
        user_data = {
            'name': name,
            'email': email,
            'education': education,
            'bio': bio,
            'job': job,
            'projects': projects,
            'passions': passions,
            'futureGoals': future_goals,
            'socialLinks': social_links,
            'resume_filename': resume_filename
        }
        result = collection.insert_one(user_data)

        print(f"✅ Successfully inserted user: {user_data}")
        return jsonify({'message': 'Portfolio submitted successfully!', 'id': str(result.inserted_id)}), 200

    except Exception as e:
        print(f"❌ Error occurred: {e}")
        return jsonify({'error': str(e)}), 500

# Route to view all portfolios
@app.route('/view_portfolios', methods=['GET'])
def view_portfolios():
    try:
        portfolios = list(collection.find({}, {'_id': 0}))
        return jsonify(portfolios), 200
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        return jsonify({'error': str(e)}), 500

# Route to clear all portfolios (Use this with caution)
@app.route('/clear_portfolios', methods=['DELETE'])
def clear_portfolios():
    try:
        result = collection.delete_many({})
        print(f"✅ Deleted {result.deleted_count} portfolios.")
        return jsonify({'message': f'Deleted {result.deleted_count} portfolios'}), 200
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        return jsonify({'error': str(e)}), 500

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
