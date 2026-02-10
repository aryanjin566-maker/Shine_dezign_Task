student = {
  "Aryan":100,
  "Rohan":95,
  "Sita":90,
  "Gita":85
}

# 1. Calculate Average
total = 0 

for marks in student.values():
  total += marks

average = total / len(student)
print("\nAverage Marks" ,  average)

topper = max(student, key=student.get)
print("\nTopper is", topper, "with marks", student[topper])

# 3. Grade for each student
print("\nGrades:")
for name, marks in student.items():
    if marks >= 90:
        grade = "A"
    elif marks >= 75:
        grade = "B"
    elif marks >= 60:
        grade = "C"
    else:
        grade = "D"
    print(name, ":", grade)