from flask import Flask, render_template, redirect
from selbst_kontrolle_script import Quiz

app = Flask(__name__)

quiz = Quiz
quiz.load_questions(quiz)

@app.route("/")
def hello_world():
    return render_template("main.html")

@app.route("/quiz/<username>")
def show_quiz(username=None):
    # returnstring, antwort, question_number, progress = quiz.get_question(quiz, username)
    daten = quiz.get_question(quiz, username)
    # print(daten.q_question)
    return render_template('quiz.html', daten = daten, username=username)

@app.route("/answer/<selection>/<username>/<questionnumber>")
def answer(selection=None,username=None,questionnumber=None):
    quiz.antwort(quiz,question_number=questionnumber, username=username,korrekt=selection)
    return redirect(f"/continue/{username}")

@app.route("/continue/<username>")
def cont(username=None):
    return render_template('continue.html', username=username)


