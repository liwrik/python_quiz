from db_scripts import get_question_after, get_quises, check_answer
from flask import Flask, redirect, url_for, session, request, render_template
from random import randint, shuffle
import os


def quiz_form():
    # html_beg = '<html><body><h2>Выберите викторину:</h2><form method="post" action = "index"><select name = "quiz">'
    # options = ' '
    # q_list = get_quises() #получаем список кортежей типа (id, name)
    # for id, name in q_list:
    #     option_line = f'<option value={id}> {name} </option>'
    #     options = options + option_line

    # frm_submit = '<p><input type = "submit" value="Выбрать"></p>'
    # html_end = f'</select>{frm_submit}</form></body></html>'
    # print(html_beg + options + html_end)
    # return html_beg + options + html_end
    q_list = get_quises()
    return render_template("start.html", q_list = q_list)


def start_quiz(quiz_id):
    session['quiz'] = quiz_id
    session['last_question'] = 0
    session["total"] = 0
    session["answers"] = 0


def end_quiz():
    session.clear()


def index():
    if request.method == 'GET':
        start_quiz(-1)
        return quiz_form()
   
    else:
        quest_id = request.form.get('quiz')
        start_quiz(quest_id)
        return redirect(url_for('test'))


def test():
    if 'quiz' not in session or int(session['quiz']) < 0:
        return redirect(url_for('index'))

    else:
        if request.method == "POST":
            save_answers()
        result = get_question_after(session["last_question"], session["quiz"])
        if result is None or len(result) == 0:
            return redirect(url_for('result'))
        else:
            return question_form(result)

def question_form(question):
    answers_list = [question[2], question[3], question[4], question[5]]
    shuffle(answers_list)
    return render_template("test.html",
            question = question[1], quest_id = question[0],
            answers_list = answers_list)

def save_answers():
    answer = request.form.get("ans_text")
    quest_id = request.form.get('q_id')
    session['last_question'] = quest_id
    session["total"] += 1
    if check_answer(quest_id, answer):
        session["answers"] += 1

def result():
    a = render_template("result.html", right = session["answers"], total = session["total"])
    end_quiz()
    return a

folder = os.getcwd()
app = Flask(__name__, static_folder = folder, template_folder = folder)
app.add_url_rule('/', 'index', index)
app.add_url_rule('/index', 'index', index, methods=['post', 'get'])
app.add_url_rule('/test', 'test', test, methods = ['post', 'get'])
app.add_url_rule('/result', 'result', result)
app.config['SECRET_KEY'] = 'Varavara'

if __name__ == '__main__':
    app.run()

