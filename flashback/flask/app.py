from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from llm_interface import get_response_for_prompt
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')

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


if __name__ == "__main__":
    app.run()
