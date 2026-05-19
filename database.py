import sqlite3

# Connect Database
conn = sqlite3.connect("users.db")

cursor = conn.cursor()

# Create Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    email TEXT,

    password TEXT
)
""")

conn.commit()

# Add User
def add_user(email, password):

    cursor.execute(
        "INSERT INTO users(email,password) VALUES(?,?)",
        (email,password)
    )

    conn.commit()

# Check Login
def login_user(email, password):

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email,password)
    )

    data = cursor.fetchone()

    return data