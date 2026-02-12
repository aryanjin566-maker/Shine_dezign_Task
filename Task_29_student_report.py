from datetime import date 

students = [{"name" : "Aryan" , "marks": 100, "grade": "A"}
           ,{"name" : "Rohan" , "marks": 95, "grade": "A"}
           ,{"name" : "Sita" , "marks": 90, "grade": "A"}
           ,{"name" : "Gita" , "marks": 85, "grade": "B"}]

with open("student_report.txt", "w") as file :
   file.write("student report:\n")
   file.write(f"\ndate: {date.today()}\n")

   for student in students:
      file.write(f"\nName : {student['name']}\n marks : {student['marks']}\n grade : {student['grade']}\n\n")

