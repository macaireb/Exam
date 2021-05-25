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
        cur.execute("CREATE TABLE IF NOT EXISTS " + exam[1][0] + '_Test' +
                    "(QType text, QorA text, number integer, body text)")
        for i in range(len(exam[0])):
            ques = exam[0][i].split() + exam[1][i].split()
            print("Inserting " + exam[0][i] + exam[1][i])
            cur.execute("INSERT INTO " + exam[1][0] + '_Test VALUES (?, ?, ?, ?)', (ques[0], ques[1], ques[2], ques[-1]))
        conn.commit()
        conn.close()