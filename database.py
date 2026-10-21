
import sqlite3

DATABASE = "students.db"


def get_db():
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    with get_db() as con:
        # Create the table if it does not exist
        con.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                department TEXT NOT NULL
            )
        """)

        # Check which columns already exist
        columns = {
            row["name"]
            for row in con.execute(
                "PRAGMA table_info(students)"
            ).fetchall()
        }

        # Add missing columns without deleting existing records
        if "email" not in columns:
            con.execute(
                "ALTER TABLE students ADD COLUMN email TEXT"
            )

        if "password" not in columns:
            con.execute(
                "ALTER TABLE students ADD COLUMN password TEXT"
            )

        # Ensure the database changes are saved
        con.commit()
