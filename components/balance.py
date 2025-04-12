# components/balance.py
import sqlite3

class BalanceCheck:
    def __init__(self, acc_num, password):
        self.acc = acc_num
        self.pa = password
        
    def print_balance(self):
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        c.execute("SELECT password, balance FROM accounts WHERE username = ?", (self.acc,))
        result = c.fetchone()
        
        if not result or result[0] != self.pa:
            conn.close()
            return Exception("Invalid Details")
            
        balance = result[1]
        conn.close()
        return balance