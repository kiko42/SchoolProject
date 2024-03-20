import sqlite3
from datetime import datetime

if __name__ == '__main__':
    connection = sqlite3.connect("SchoolDatabase.db")
    cursor = connection.cursor()
    print('-' * 20, 'Welcome to the School Management Program', '-' * 20)
    Value = True
    while Value:
        print('Note: enter Done to close the program')
        Letter = input("Enter the letter to do an operation:")
        Letter = Letter.upper()
        if Letter == 'A':
            print('-' * 10, 'You entered A to sign up a new student', '-' * 20)
            StudentName = input("Enter the Student Name:")
            StudentNickname = input("Enter the Student Nickname:")
            StudentClass = input("Enter the Student Class:")
            StudentAge = input("Enter the Student Age:")
            StudentRegistrationDate = datetime.now().strftime("%Y-%m-%d")
            cursor.execute("INSERT INTO Students (Name, NickName, Age, Class, RegistrationDate) VALUES (?, ?, ?, ?, ?)",
                           (StudentName, StudentNickname, StudentAge, StudentClass, StudentRegistrationDate))
            connection.commit()
            print('Done')
        elif Letter == 'D':
            print('-' * 10, 'You entered D to delete a student', '-' * 20)
            StudentID = input("Enter the student ID:")
            StudentExistence = cursor.execute("SELECT * FROM Students WHERE StudentID = ?", (StudentID,)).fetchone()
            if StudentExistence is None:
                print('There is no Student with this ID')
            else:
                cursor.execute("DELETE FROM Students WHERE StudentID = ?", (StudentID,))
                connection.commit()
            print('Done')
        elif Letter == 'U':
            print('-' * 10, 'You entered U to update a student information', '-' * 20)
            StudentID = input("Enter the student ID:")
            StudentExistence = cursor.execute("SELECT * FROM Students WHERE StudentID = ?", (StudentID,)).fetchone()
            if StudentExistence is None:
                print('There is no Student with this ID or may it has been deleted')
            else:
                StudentName = input("Enter the New Student Name:")
                StudentNickname = input("Enter the New Student Nickname:")
                StudentClass = input("Enter the New Student Class:")
                StudentAge = input("Enter the New Student Age:")
                cursor.execute(
                    "UPDATE Students SET Name = ?, Nickname = ?, Class = ?, Age = ? WHERE StudentID = ?",
                    (StudentName, StudentNickname, StudentClass, StudentAge, StudentID))
                connection.commit()
                print('Done')
        elif Letter == 'S':
            print('-' * 10, 'You entered U to view a student information', '-' * 20)
            StudentID = input("Enter the student ID:")
            StudentInfo = cursor.execute("SELECT * FROM Students WHERE StudentID = ?", (StudentID,)).fetchone()
            print('='*20, 'The Student information', '='*20)
            print(StudentInfo)
            print('=' * 65)
        elif Letter == 'DONE':
            Value = False
        else:
            print(
                "The letter you entered does not execute any operation\nTo perform an operation، Please choose one of the following letters:\n A -> Sing up a new student\n D -> Delete a student from the database\n U -> Update a student information\n S -> view a student information")
    connection.commit()
    cursor.close()
    connection.close()
