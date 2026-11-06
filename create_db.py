import sqlite3

connection = sqlite3.connect("demo.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    group_name TEXT NOT NULL,
    age INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    hours INTEGER NOT NULL
)
""")

cursor.execute("DELETE FROM students")
cursor.execute("DELETE FROM subjects")

cursor.executemany(
    "INSERT INTO students (name, group_name, age) VALUES (?, ?, ?)",
    [
        ("Anna Petrova", "6133", 21),
        ("Ivan Smirnov", "6133", 22),
        ("Maria Volkova", "6134", 20),
        ("Pavel Orlov", "6134", 21)
    ]
)

cursor.executemany(
    "INSERT INTO subjects (title, hours) VALUES (?, ?)",
    [
        ("GUI Design", 72),
        ("Databases", 108),
        ("Machine Learning", 144)
    ]
)

cursor.execute(
    "CREATE INDEX IF NOT EXISTS idx_students_group "
    "ON students(group_name)"
)

connection.commit()
connection.close()

print("demo.db created")
