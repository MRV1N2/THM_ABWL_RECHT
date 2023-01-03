from flask import Flask
from flask import render_template
from selbst_kontrolle_script import Quiz

app = Flask(__name__)

quiz = Quiz
quiz.load_questions(quiz)

@app.route("/")
def hello_world():
    return render_template("main.html")

@app.route("/quiz/<username>")
def show_quiz(username=None):
    returnstring, antwort, question_number, progress = quiz.get_question(quiz, username)
    return render_template('quiz.html', string = returnstring)

