from flask import Flask, request, render_template, url_for
import requests, json
import random, config

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        num = request.form['num']
        return "Starting game"
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)