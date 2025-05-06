from flask import Flask, render_template
import json
import random 

app = Flask(__name__)


class Question:
    def __init__(self, question, answer, options):
        self.question = question
        self.index = 0
        self.answer = answer
        self.options = options

    def load_information(self, path):
        with open(path, 'r', encoding= 'utf-8') as f:
            return json.loads(f.read())
        
    def get_set_of_questions(self, path):
        questions = self.load_information(path)
        question_list = []
        for question in questions:
            question_list.append(Question(question["question"], question["answer"], question["options"]))
        return question_list

@app.route("/")
def home():
    message = "Hello you are Thomas"
    signe  = 0 
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

    # Load the JSON file to check if it is valid
    question = Question("", "", [])

    print(question.load_information("categories/films.json"))
    

    app.run(debug=True)
