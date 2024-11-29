from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database connection for the login system
def create_login_connection():
    return sqlite3.connect("login.db")

# Database connection for the dashboard (expenses)
def create_dashboard_connection():
    return sqlite3.connect("dashboard.db")

# Create login table
def create_login_table():
    conn = create_login_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS login (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            number TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Create dashboard table
def create_dashboard_table():
    conn = create_dashboard_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dashboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expenditure TEXT NOT NULL,
            amount REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get user input
        name = request.form['email']
        password = request.form['password']

        # Verify login credentials
        conn = create_login_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM login WHERE name = ? AND number = ?", (name, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get user input
        name = request.form['email1']
        password = request.form['password1']

        # Save to database
        conn = create_login_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO login (name, number) VALUES (?, ?)", (name, password))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        # Get user input
        expense_name = request.form['expense_name']
        expense_amount = request.form['expense_amount']

        # Save to database
        conn = create_dashboard_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO dashboard (expenditure, amount) VALUES (?, ?)", (expense_name, expense_amount))
        conn.commit()
        conn.close()

    # Retrieve all expenses
    conn = create_dashboard_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT expenditure, amount FROM dashboard")
    expenses = cursor.fetchall()
    conn.close()

    total_expense = sum(amount for _, amount in expenses)

    return render_template('dashboard.html', expenses=expenses, total_expense=total_expense)

if __name__ == '__main__':
    # Initialize databases
    create_login_table()
    create_dashboard_table()
    app.run(debug=True)
