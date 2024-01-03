import sqlite3
db_name = 'quiz.sqlite'
conn = None
curor = None




def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()




def close():
    cursor.close()
    conn.close()




def do(query):
    cursor.execute(query)
    conn.commit()




def clear_db():
    ''' удаляет все таблицы '''
    open()
    query = '''DROP TABLE IF EXISTS quiz_content'''
    do(query)
    query = '''DROP TABLE IF EXISTS question'''
    do(query)
    query = '''DROP TABLE IF EXISTS quiz'''
    do(query)
    close()




   
def create():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
   
    do('''CREATE TABLE IF NOT EXISTS quiz(
       id INTEGER PRIMARY KEY,
       name VARCHAR)''')




    do('''CREATE TABLE IF NOT EXISTS question(
       id INTEGER PRIMARY KEY,
       question VARCHAR,
       answer VARCHAR,
       wrong1 VARCHAR,
       wrong2 VARCHAR,
       wrong3 VARCHAR)''')




    do('''CREATE TABLE IF NOT EXISTS quiz_content(
       id INTEGER PRIMARY KEY,
       quiz_id INTEGER,
       question_id INTEGER,
       FOREIGN KEY (quiz_id) REFERENCES quiz (id),
       FOREIGN KEY (question_id) REFERENCES question (id) )''')
    close()




def add_questions():
    questions = [
        ('Сколько месяцев в году имеет 28 дней?', 'Все', 'Один', 'Два', 'Ни одного'),
        ('Сколько будет 2*0', 'Ноль', 'Два', 'Двадцать', 'Один'),
        ('Сколько будет 2+2*2', 'Шесть', 'Восемь', 'Двадцать четыре', 'Две тысячи двадвать два'),
        ('Пойдем в пятерочка?','Я Толя','Ну го','Ура пятерочка', 'Нет'),
        ('Как называется сказка про царя и сына его?','Сказка о царе Салтане','По щучьему веленью','Лягушка-путешественница','Царевна лягушка'),
        ('Каких камней нет в море?','Сухих','Острых','Гладких','Красных'),
        ('Чему равен корень из 25?','5','8','не извлекается','12,5'),
        ('Лучший язык программирования в 2023 году?','Python','C#','C++','JavaScript')
    ]




    open()
    cursor.executemany('''INSERT INTO question
    (question, answer, wrong1, wrong2, wrong3)
    VALUES (?, ?, ?, ?, ?)''', questions)




    conn.commit()
    close()




def add_quiz():
    quizes = [
        ('Своя игра',),
        ('Кто хочет стать миллионером?',),
    ]




    open()
    cursor.executemany('''INSERT INTO quiz
    (name)
    VALUES (?)''', quizes)
    conn.commit()
    close()


def add_links():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
    query = "INSERT INTO quiz_content (quiz_id, question_id) VALUES (?, ?)"
    answer = input("Добавить связь (y/n)")
    while answer != 'n':
        quiz_id = int(input('id ВИК:'))
        question_id = int(input('id ВОПР:'))
        cursor.execute(query, [quiz_id, question_id])
        conn.commit()
        answer = input("Добавить связь (y/n)")


    close()


def get_question_after(question_id = 0, quiz_id = 1):
    open()
    query = '''
SELECT quiz_content.id, question.question, question.answer,
question.wrong1, question.wrong2, question.wrong3
FROM question, quiz_content
WHERE quiz_content.quiz_id == ?
AND quiz_content.question_id == question.id
AND quiz_content.question_id > ?
ORDER BY quiz_content.question_id'''


    cursor.execute(query, [quiz_id, question_id])
    result = cursor.fetchone()
    close()
    return result




def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    print(cursor.fetchall())
    close()




def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')




def main():
    clear_db()
    create()
    add_questions()
    add_quiz()
    add_links()
    show_tables()
    # res = get_question_after(2, 1)
    # print()s
    # print(res)


def get_quises():
    open()
    query = 'SELECT * FROM quiz ORDER BY id'
    cursor.execute(query)
    result = cursor.fetchall()
    close()
    return result


def check_answer(q_id, ans_text):
    query = '''SELECT question.answer
               FROM quiz_content, question
               WHERE quiz_content.id = ?
               AND quiz_content.question_id = question_id'''
    
    open()
    cursor.execute(query, str(q_id))
    result = cursor.fetchone()
    close()

    if result[0] == ans_text:
        return True

if __name__ == "__main__":
    main()