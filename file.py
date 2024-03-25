import sqlite3
from datetime import datetime

if __name__ == "__main__":
    connection = sqlite3.connect("SchoolDatabase.db")
    cursor = connection.cursor()

    studentlesson = "-1"
    print(bool(cursor.execute("SELECT EXISTS (SELECT 1 FROM Lessons WHERE LessonID = ?)",
                                                       (studentlesson,)).fetchone()[0]))

    connection.commit()
    cursor.close()
    connection.close()
