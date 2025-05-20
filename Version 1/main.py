from flask import Flask, render_template
import json
import random 

app = Flask(__name__)


def load_information(path):
    with open(path, 'r', encoding= 'utf-8') as f:
        return json.loads(f.read())


@app.route("/")
def home():
    questions = load_information("categories/films.json")
    message = "Hello you are Thomas"
    signe  = 0 
    print(questions)
    return render_template("index.html", message = message, signe = signe)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/quiz")
def quiz():
    return render_template("quiz.html")

@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/result")
def result():
    return render_template("result.html")

@app.route("/error")
def error():
    return render_template("error.html")


if __name__ == "__main__":
    
    app.run(debug=True)
