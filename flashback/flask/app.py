from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from llm_interface import get_response_for_prompt
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
	print(os.environ.get('FLASK_SECRET_KEY'), " is the secret key")
	return render_template('index.html')

@app.route('/handle_prompt', methods = ["POST"])
def handle_prompt():
	response = get_response_for_prompt(request.form.get('prompt'))
	flash(response)
	return redirect(url_for('index'))

@app.route('/flask-health-check')
def flask_health_check():
	return "success"

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['video']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = file.filename
        if not os.path.isdir(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({"message": "Video uploaded successfully!", "filename": filename}), 201
    
    return jsonify({"error": "File type not allowed"}), 400


if __name__ == "__main__":
    app.run()
