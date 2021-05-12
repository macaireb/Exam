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