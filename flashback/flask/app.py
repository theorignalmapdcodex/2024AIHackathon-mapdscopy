from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def hello():
	return render_template('index.html')

@app.route('/info')
def info():

	resp = {
		'connecting_ip': request.headers['X-Real-IP'],
		'proxy_ip': request.headers['X-Forwarded-For'],
		'host': request.headers['Host'],
		'user-agent': request.headers['User-Agent']
	}

	return jsonify(resp)

@app.route('/flask-health-check')
def flask_health_check():
	return "success"


if __name__ == "__main__":
    app.run()
