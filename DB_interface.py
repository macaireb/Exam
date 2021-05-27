import sqlite3


class DB_interface():

    def get_users(self):
        conn = sqlite3.connect("storage.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        tmp = cur.fetchall()
        conn.close()
        return tmp

    def add_user(self, fn, ln):
        conn = sqlite3.connect("storage.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO users VALUES (?, ?)", (fn, ln))
        conn.commit()
        conn.close()

    def save_exam(self, exam):
        conn = sqlite3.connect("storage.db")
        cur = conn.cursor()
        exam[1][0] = exam[1][0].replace(' ', '_')
        cur.execute("CREATE TABLE IF NOT EXISTS " + exam[1][0] + '_Test' +
                    "(QType text, QorA text, number integer, body text)")
        for i in range(len(exam[0])):
            ques = exam[0][i].split() + exam[1][i].split()
            print("Inserting " + exam[0][i] + exam[1][i])
            cur.execute("INSERT INTO " + exam[1][0] + '_Test VALUES (?, ?, ?, ?)', (ques[0], ques[1], ques[2], ques[-1]))
        conn.commit()
        conn.close()

    def get_exams_list(self):
        exams = []
        placeholder = []
        conn = sqlite3.connect("storage.db")
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        placeholder = cur.fetchall()
        conn.close()
        for i in placeholder:
            if i[0].endswith('_Test'):
                exams.append(i)
        return exams

    def get_single_exam(self, name):
        exam = []
        conn = sqlite3.connect("storage.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM " + name)
        exam = cur.fetchall()
        conn.close()
        return exam
