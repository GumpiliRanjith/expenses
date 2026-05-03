from flask import Flask, render_template, request, redirect
import sqlite3

application  = Flask(__name__)

# Create DB
def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Home page
@application.route('/')
def index():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT * FROM expenses")
    expenses = c.fetchall()

    total = sum([e[1] for e in expenses])

    conn.close()
    return render_template('index.html', expenses=expenses, total=total)

# Add expense
@application.route('/add', methods=['POST'])
def add():
    amount = request.form['amount']
    category = request.form['category']
    date = request.form['date']

    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
              (amount, category, date))
    conn.commit()
    conn.close()

    return redirect('/')

# Delete expense
@application.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    application.run()
