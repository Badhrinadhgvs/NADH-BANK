import streamlit as st
from components.newaccount import CreateNewAccount
from components.debit import DebitAmt
from components.credit import CreditAmt
from components.balance import BalanceCheck
import sqlite3

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS accounts 
                 (username TEXT PRIMARY KEY, password TEXT, balance REAL)''')
    conn.commit()
    conn.close()

# Initialize session state for page control
if "page" not in st.session_state:
    st.session_state.page = "home"

# Page functions
def home_page():
    st.title("🏧 Nadh Bank ATM Interface")
    st.subheader("Welcome! Choose an operation:")
    
    # Create four columns for the buttons
    col1, col2, col3, col4 = st.columns(4)
    
    # Place each button in its own column
    with col1:
        if st.button("📝 Create Account", key="btn_create"):
            st.session_state.page = "create"
    with col2:
        if st.button("💰 Deposit Money", key="btn_deposit"):
            st.session_state.page = "deposit"
    with col3:
        if st.button("🏧 Withdraw Money", key="btn_withdraw"):
            st.session_state.page = "withdraw"
    with col4:
        if st.button("📊 Check Balance", key="btn_balance"):
            st.session_state.page = "balance"
def create_account():
    st.title("📝 Create New Bank Account")
    name = st.text_input("Account Name", key="create_name")
    password = st.text_input("Password", type="password", key="create_pass")
    deposit = st.number_input("Initial Deposit", min_value=0.0, step=1.0, key="create_deposit")

    if st.button("Create Account", key="create_btn"):
        account = CreateNewAccount(name, deposit, password)
        if account.create():
            st.success("✅ Account Created Successfully!")
        else:
            st.error("❌ Account already exists or invalid details.")

    if st.button("🔙 Back to Home", key="back_create"):
        st.session_state.page = "home"

def deposit_money():
    st.title("💰 Deposit Money")
    name = st.text_input("Account Name", key="deposit_name")
    password = st.text_input("Password", type="password", key="deposit_pass")
    amount = st.number_input("Deposit Amount", min_value=0.0, step=1.0, key="deposit_amt")

    if st.button("Deposit", key="deposit_btn"):
        debit = DebitAmt(amount, name, password)
        result = debit.debit_amt()
        if isinstance(result, Exception):
            st.error(str(result))
        else:
            st.success(f"✅ Amount Deposited! New Balance: Rs.{result}")

    if st.button("🔙 Back to Home", key="back_deposit"):
        st.session_state.page = "home"

def withdraw_money():
    st.title("🏧 Withdraw Money")
    name = st.text_input("Account Name", key="withdraw_name")
    password = st.text_input("Password", type="password", key="withdraw_pass")
    amount = st.number_input("Withdrawal Amount", min_value=0.0, step=1.0, key="withdraw_amt")

    if st.button("Withdraw", key="withdraw_btn"):
        credit = CreditAmt(amount, name, password)
        result = credit.credit_amt()
        if isinstance(result, Exception):
            st.error(str(result))
        else:
            st.success(f"✅ Amount Withdrawn! New Balance: Rs.{result}")

    if st.button("🔙 Back to Home", key="back_withdraw"):
        st.session_state.page = "home"

def check_balance():
    st.title("📊 Check Account Balance")
    name = st.text_input("Account Name", key="balance_name")
    password = st.text_input("Password", type="password", key="balance_pass")

    if st.button("Check Balance", key="balance_btn"):
        balance = BalanceCheck(name, password)
        result = balance.print_balance()
        if isinstance(result, Exception):
            st.error(str(result))
        else:
            st.success(f"✅ Available Balance: Rs.{result}")

    if st.button("🔙 Back to Home", key="back_balance"):
        st.session_state.page = "home"

# Main Streamlit app
def main():
    init_db()

    # Navigate based on session state
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "create":
        create_account()
    elif st.session_state.page == "deposit":
        deposit_money()
    elif st.session_state.page == "withdraw":
        withdraw_money()
    elif st.session_state.page == "balance":
        check_balance()

if __name__ == "__main__":
    main()
