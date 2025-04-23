import sqlite3
from datetime import datetime

DB_NAME = "finance.db"

def connect():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = connect()
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            amount REAL,
            category TEXT,
            date TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            amount REAL,
            category TEXT,
            date TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS savings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            date TEXT
        )
    ''')

    conn.commit()
    conn.close()

# ---------- User ----------
def register_user(username, email, password):
    try:
        conn = connect()
        c = conn.cursor()
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(email, password):
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = c.fetchone()
    conn.close()
    return user

def update_profile(user_id, username, email, password):
    conn = connect()
    c = conn.cursor()
    c.execute("UPDATE users SET username = ?, email = ?, password = ? WHERE id = ?", (username, email, password, user_id))
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id = ?", (user_id,))
    c.execute("DELETE FROM income WHERE user_id = ?", (user_id,))
    c.execute("DELETE FROM expenses WHERE user_id = ?", (user_id,))
    c.execute("DELETE FROM savings WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

# ---------- Income ----------
def add_income(user_id, title, amount, category, date):
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO income (user_id, title, amount, category, date) VALUES (?, ?, ?, ?, ?)",
              (user_id, title, amount, category, date))
    conn.commit()
    conn.close()

def get_income(user_id):
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM income WHERE user_id = ?", (user_id,))
    income = c.fetchall()
    conn.close()
    return income

def delete_income(income_id):
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM income WHERE id = ?", (income_id,))
    conn.commit()
    conn.close()

# ---------- Expenses ----------
def add_expense(user_id, title, amount, category, date):
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO expenses (user_id, title, amount, category, date) VALUES (?, ?, ?, ?, ?)",
              (user_id, title, amount, category, date))
    conn.commit()
    conn.close()

def get_expenses(user_id):
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM expenses WHERE user_id = ?", (user_id,))
    expenses = c.fetchall()
    conn.close()
    return expenses

def delete_expense(expense_id):
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()

# ---------- Savings ----------
def add_saving(user_id, amount, date):
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO savings (user_id, amount, date) VALUES (?, ?, ?)", (user_id, amount, date))
    conn.commit()
    conn.close()

def get_savings(user_id):
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM savings WHERE user_id = ?", (user_id,))
    savings = c.fetchall()
    conn.close()
    return savings

def delete_saving(saving_id):
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM savings WHERE id = ?", (saving_id,))
    conn.commit()
    conn.close()


