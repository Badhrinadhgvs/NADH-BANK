# components/newaccount.py
import sqlite3

class CreateNewAccount:
    def __init__(self, name, deposit, pa):
        self.name = name
        self.dep = deposit
        self.pa = pa
        
    def create(self):
        try:
            conn = sqlite3.connect('bank.db')
            c = conn.cursor()
            c.execute("INSERT INTO accounts (username, password, balance) VALUES (?, ?, ?)",
                     (self.name, self.pa, self.dep))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False