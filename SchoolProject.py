import sqlite3
from datetime import datetime

if __name__ == "__main__":
    connection = sqlite3.connect("SchoolDatabase.db")
    cursor = connection.cursor()
    print("-" * 40, "Welcome to the School Management Program", "-" * 40)
    Value = True
    while Value:
        print("| _______________________________________________________________________|")
        print("| To perform an operation، please choose one of the following choices:   |")
        print("| 'A'  -> Add a new student.                                             |")
        print("| 'D'  -> Delete a student from the database.                            |")
        print("| 'U'  -> Update a student information.                                  |")
        print("| 'V'  -> view a student information.                                    |")
        print("| 'Done' to close the program.                                           |")
        print("| _______________________________________________________________________|")
        Letter = input("Enter somthing to do an operation:").capitalize()
        if Letter == "A":
            print("-" * 10, "You entered A to Add a new student", "-" * 20)
            Boolan = True
            while Boolan:
                StudentName = input("Enter the Student Name:").capitalize()
                if StudentName.isalpha():
                    break
                else:
                    print("The student name can't contain numbers, spaces, emojis, symbols or be empty.")
            while Boolan:
                StudentNickname = input("Enter the Student Nick Name:").capitalize()
                if StudentNickname.isalpha():
                    break
                else:
                    print("The student nickname can't contain numbers, spaces, emojis, symbols or be empty.")
            Boolean = True
            while Boolean:
                print(
                    "The classes in this school are between 1st and 4th class, please enter 1, 2, 3, 4 or first, second, third, fourth.")
                StudentClass = input("Enter the Student Class:").capitalize()
                if StudentClass == "1" or StudentClass == "First":
                    StudentClass = "1st"
                    break
                elif StudentClass == "2" or StudentClass == "Second":
                    StudentClass = "2nd"
                    break
                elif StudentClass == "3" or StudentClass == "Third":
                    StudentClass = "3rd"
                    break
                elif StudentClass == "4" or StudentClass == "Fourth":
                    StudentClass = "4th"
                    break
                else:
                    print("Invalid input.")
            while Boolan:
                StudentAge = input("Enter the Student Age:")
                if StudentAge.isdigit():
                    StudentAge = int(StudentAge)
                    if 17 <= StudentAge <= 24:
                        break
                    else:
                        print("The student age should to be between 17 and 24.")
                else:
                    print(
                        "The student age can't be empty or contain spaces...etc.., it should to be an integer number.")
            StudentRegistrationDate = datetime.now().strftime("%Y-%m-%d")
            cursor.execute("INSERT INTO Students (Name, NickName, Age, Class, RegistrationDate) VALUES (?, ?, ?, ?, ?)",
                           (StudentName, StudentNickname, StudentAge, StudentClass, StudentRegistrationDate))
            Boolan = True
            print("-" * 110)
            print(
                "You sign up a new student, now you should to give this student at least 1 lesson of the following lessons:")
            LessonsList = cursor.execute("SELECT * FROM Lessons").fetchall()
            LessonsList = [[row[0], row[1], row[2]] for row in LessonsList]
            x = 0
            for lesson in LessonsList:
                x += 1
                print(f"Lesson {x}:\nThe lesson ID: {lesson[0]}\nThe lesson: {lesson[1]} \nThe teacher: {lesson[2]}")
                print('=' * 65)
            while Boolan:
                HowMuchLessons = input("How much lessons you want to add to this student:")
                if HowMuchLessons.isdigit():
                    HowMuchLessons = int(HowMuchLessons)
                    if 0 < HowMuchLessons <= len(LessonsList):
                        for x in range(HowMuchLessons):
                            while Boolan:
                                StudentLessonID = input("Enter a lesson id:")
                                value1 = bool(cursor.execute("SELECT EXISTS (SELECT 1 FROM Lessons WHERE LessonID = ?)",
                                                             (StudentLessonID,)).fetchone()[0])
                                StudentID = \
                                    cursor.execute(
                                        "SELECT StudentID FROM Students ORDER BY StudentID DESC LIMIT 1").fetchone()[
                                        0]
                                LessonsIDs = cursor.execute("SELECT LessonID FROM StudentLessons WHERE StudentID = ?",
                                                            (StudentID,)).fetchall()
                                LessonsIDs = ' '.join(str(row[0]) for row in LessonsIDs)
                                LessonsIDs = LessonsIDs.split(" ")
                                value2 = StudentLessonID not in LessonsIDs
                                if value1 and value2:
                                    cursor.execute("INSERT INTO StudentLessons (StudentID, LessonID) VALUES (?, ?)",
                                                   (StudentID, StudentLessonID))
                                    connection.commit()
                                    break
                                else:
                                    print("You can't enter a string or symbol...etc...")
                                    print("You can't add a lessonId that is not existed.")
                                    print("You can't add a lesson that been given to the student before.")
                        break
                    else:
                        print(f"You should enter a number between 1 and {len(LessonsList)}")
                else:
                    print("You should to enter an integer number.")
            print("Done")
        elif Letter == "D":
            print('-' * 10, 'You entered D to delete a student', '-' * 20)
            StudentID = input("Enter the student ID:")
            StudentExistence = cursor.execute("SELECT * FROM Students WHERE StudentID = ?", (StudentID,)).fetchone()
            if StudentExistence is None:
                print('There is no Student with this ID')
            else:
                cursor.execute("DELETE FROM StudentLessons WHERE StudentID = ?", (StudentID,))
                cursor.execute("DELETE FROM Students WHERE StudentID = ?", (StudentID,))
                connection.commit()
            print("Done")
        elif Letter == "U":
            print('-' * 10, 'You entered U to update a student information', '-' * 20)
            StudentID = input("Enter the student ID:")
            StudentExistence = cursor.execute("SELECT * FROM Students WHERE StudentID = ?", (StudentID,)).fetchone()
            if StudentExistence is None:
                print('There is no Student with this ID or may it has been deleted')
            else:
                StudentName1 = cursor.execute("SELECT Name FROM Students WHERE StudentID = ?", (StudentID,)).fetchone()[
                    0]
                StudentNickname1 = \
                    cursor.execute("SELECT NickName FROM Students WHERE StudentID = ?", (StudentID,)).fetchone()[0]
                StudentClass1 = \
                    cursor.execute("SELECT Class FROM Students WHERE StudentID = ?", (StudentID,)).fetchone()[0]
                StudentAge1 = cursor.execute("SELECT Age FROM Students WHERE StudentID = ?", (StudentID,)).fetchone()[0]
                Boolan = True
                print("Note: please enter hit directly if you don't want to change somthing.")
                StudentName = input("Enter the New Student Name:").capitalize()
                if StudentName == "":
                    StudentName = StudentName1
                else:
                    while Boolan:
                        if StudentName.isalpha():
                            break
                        else:
                            print("The student name can't contain numbers, spaces, emojis, symbols or be empty.")
                StudentNickname = input("Enter the New Student Nickname:").capitalize()
                if StudentNickname == "":
                    StudentNickname = StudentNickname1
                else:
                    while Boolan:
                        if StudentNickname.isalpha():
                            break
                        else:
                            print("The student nickname can't contain numbers, spaces, emojis, symbols or be empty.")
                StudentClass = input("Enter the New Student Class:").capitalize()
                if StudentClass == "":
                    StudentClass = StudentClass1
                else:
                    while Boolan:
                        print(
                            "The classes in this school are between 1st and 4th class, please enter 1, 2, 3, 4 or first, second, third, fourth.")
                        StudentClass = input("Enter the Student Class:").capitalize()
                        if StudentClass == "1" or "First":
                            StudentClass = "1st"
                            break
                        elif StudentClass == "2" or "Second":
                            StudentClass = "2nd"
                            break
                        elif StudentClass == "3" or "Third":
                            StudentClass = "3rd"
                            break
                        elif StudentClass == "4" or "Fourth":
                            StudentClass = "4th"
                            break
                        else:
                            print("invalid input.")
                while Boolan:
                    StudentAge = input("Enter the New Student Age:")
                    if StudentAge == "":
                        StudentAge = StudentAge1
                        break
                    else:
                            if StudentAge.isdigit():
                                StudentAge = int(StudentAge)
                                if 17 <= StudentAge <= 24:
                                    break
                                else:
                                    print("The student age should to be between 17 and 24.")
                            else:
                                print(
                                    "The student age can't contain spaces, symbols...etc.., it should to be an integer number.")
                cursor.execute("UPDATE Students SET Name = ?, Nickname = ?, Class = ?, Age = ? WHERE StudentID = ?",
                               (StudentName, StudentNickname, StudentClass, StudentAge, StudentID))
                connection.commit()
                print('Done')
                # ==========================================================
                # Add or remove lessons to the student, the student should at least have one lesson allways, you can't add the same lesson 2 times.
                print("_" * 5, "Update the student lessons", "_" * 50)
                print("-" * 5, "Those are the current student lessons:", "-" * 30)
                LessonsIDs = cursor.execute("SELECT LessonID FROM StudentLessons WHERE StudentID = ?",
                                            (StudentID,)).fetchall()
                LessonsIDs = ' '.join(str(row[0]) for row in LessonsIDs)
                LessonsIDs = LessonsIDs.split(" ")
                LessonTeacher = []
                for LID in LessonsIDs:
                    lessonteacher = []
                    Lesson = cursor.execute("SELECT Lesson FROM Lessons WHERE LessonID = ?", (LID,)).fetchall()[0]
                    print("ah")
                    Teacher = cursor.execute("SELECT Teacher FROM Lessons WHERE LessonID = ?", (LID,)).fetchall()[0]
                    lessonteacher.append(Lesson)
                    lessonteacher.append(Teacher)
                    LessonTeacher.append(lessonteacher)
                LesTea = [[item[0] for item in sublist] for sublist in LessonTeacher]
                LessonTeacher = LesTea
                x = 0
                for lesson in LessonTeacher:
                    x += 1
                    print(f"Lesson {x}:\nThe lesson: {lesson[0]} \nThe teacher: {lesson[1]}")
                print('=' * 65)
                print("-" * 5, "Those are the current available lessons to subscribe to:", "-" * 30)
                LessonsList = cursor.execute("SELECT * FROM Lessons").fetchall()
                LessonsList = [[row[0], row[1], row[2]] for row in LessonsList]
                x = 0
                for lesson in LessonsList:
                    x += 1
                    print(
                        f"Lesson {x}:\nThe lesson ID: {lesson[0]}\nThe lesson: {lesson[1]} \nThe teacher: {lesson[2]}")
                    print('=' * 65)
                print("-" * 100)
                print(
                    "If you don't want to add or delete a lesson for the student or you done doing that hit enter directly .")
                print("Enter one of the student lessons ID to delete it from his lessons list.")
                print("Enter a lesson ID that is not in the student lessons list if you want to add it to his list.")
                print("-" * 100)
                while Boolan:
                    studentlesson = input("Enter:")
                    if studentlesson == "":
                        break
                    elif studentlesson.isdigit():
                        IsItNone = bool(cursor.execute("SELECT EXISTS (SELECT 1 FROM Lessons WHERE LessonID = ?)",
                                                       (studentlesson,)).fetchone()[0])
                        if IsItNone is None:
                            print("Enter a correct lesson ID or hit enter directly.")
                        elif bool(cursor.execute("SELECT EXISTS (SELECT 1 FROM StudentLessons WHERE StudentID = ? AND LessonID = ?)", (StudentID, studentlesson)).fetchone()[0]) and len(cursor.execute("SELECT * FROM StudentLessons WHERE StudentID = ? ", (StudentID,)).fetchall()) <= 1:
                            print("This Student has this lesson only so you can't delete it.")
                        elif bool(cursor.execute("SELECT EXISTS (SELECT 1 FROM StudentLessons WHERE StudentID = ? AND LessonID = ?)", (StudentID, studentlesson)).fetchone()[0]):
                            cursor.execute("DELETE FROM StudentLessons WHERE StudentID = ? AND LessonID = ?", (StudentID, studentlesson))
                            connection.commit()
                            print("The lesson successfully deleted.")
                        else:
                            cursor.execute("INSERT INTO StudentLessons VALUES (?, ?)", (StudentID, studentlesson))
                            connection.commit()
                            print("The student successfully added.")
                    else:
                        print("You should hit enter directly or enter an integer number as a lesson ID.")
                print("Done")

        elif Letter == "V":
            print('-' * 10, 'You entered S to view a student information', '-' * 20)
            StudentID = input("Enter the student ID:")
            StudentInfo = cursor.execute("SELECT * FROM Students WHERE StudentID = ?", (StudentID,)).fetchone()
            if StudentInfo is None:
                print("There is no Student with this ID")
            else:
                StudentName = cursor.execute("SELECT Name FROM Students WHERE StudentID = ?", (StudentID,)).fetchone()[
                    0]
                StudentNickname = \
                    cursor.execute("SELECT Nickname FROM Students WHERE StudentID = ?", (StudentID,)).fetchone()[0]
                StudentAge = cursor.execute("SELECT Age FROM Students WHERE StudentID = ?", (StudentID,)).fetchone()[0]
                StudentClass = \
                    cursor.execute("SELECT Class FROM Students WHERE StudentID = ?", (StudentID,)).fetchone()[0]
                StudentRegistrationDate = \
                    cursor.execute("SELECT RegistrationDate FROM Students WHERE StudentID = ?",
                                   (StudentID,)).fetchone()[0]
                print('=' * 20, 'The Student information', '=' * 20)
                print(f"Name: {StudentName}")
                print(f"Nickname: {StudentNickname}")
                print(f"Age: {StudentAge}")
                print(f"Class: {StudentClass}")
                print(f"RegistrationDate: {StudentRegistrationDate}")
                print("-"*20, "The student lessons", "-"*20)
                LessonsIDs = cursor.execute("SELECT LessonID FROM StudentLessons WHERE StudentID = ?",
                                            (StudentID,)).fetchall()
                LessonsIDs = ' '.join(str(row[0]) for row in LessonsIDs)
                LessonsIDs = LessonsIDs.split(" ")
                LessonTeacher = []
                for LID in LessonsIDs:
                    lessonteacher = []
                    Lesson = cursor.execute("SELECT Lesson FROM Lessons WHERE LessonID = ?", (LID,)).fetchall()[0]
                    Teacher = cursor.execute("SELECT Teacher FROM Lessons WHERE LessonID = ?", (LID,)).fetchall()[0]
                    lessonteacher.append(Lesson)
                    lessonteacher.append(Teacher)
                    LessonTeacher.append(lessonteacher)
                LesTea = [[item[0] for item in sublist] for sublist in LessonTeacher]
                LessonTeacher = LesTea
                x = 0
                for lesson in LessonTeacher:
                    x += 1
                    print(f"Lesson {x}:\nThe lesson: {lesson[0]} \nThe teacher: {lesson[1]}")
                print('=' * 65)
        elif Letter == "Done":
            Value = False
        else:
            print("Invalid input.")
    connection.commit()
    cursor.close()
    connection.close()
