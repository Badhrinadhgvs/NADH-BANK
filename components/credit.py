# components/credit.py
import sqlite3

class CreditAmt:
    def __init__(self, amt, acc_num, password):
        self.amt = amt
        self.acc = acc_num
        self.pa = password
        
    def credit_amt(self):
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        c.execute("SELECT password, balance FROM accounts WHERE username = ?", (self.acc,))
        result = c.fetchone()
        
        if not result or result[0] != self.pa:
            conn.close()
            return Exception("Invalid Details")
            
        current_balance = result[1]
        if current_balance < self.amt:
            conn.close()
            return Exception("Insufficient funds")
            
        new_balance = current_balance - self.amt
        c.execute("UPDATE accounts SET balance = ? WHERE username = ?",
                 (new_balance, self.acc))
        conn.commit()
        conn.close()
        return new_balance