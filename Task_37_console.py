class student :
    def input_student_details(self):
        self.name = input("Enter student name: ")
        self.marks = int(input("Enter student marks: "))
        self.class_name = input("Enter class name: ")
        self.roll_no = int(input("Enter roll number: "))
       
    def calculate_grade(self):
        if self.marks >= 90:
            return "A"
        elif self.marks >= 75:
            return "B"
        elif self.marks >= 60:
            return "C"
        else:
            return "D"
    
    def display_result(self):
        grade = self.calculate_grade()
        print("\nStudent Result:") 
        print(f"Grade: {grade}")

while True:
    i = 1
    student_id = student()
    student_id.input_student_details()
    student_id.display_result()

    with open("student_results.txt", "w") as file:
        file.write(f"\nStudent {i}:\n")
        file.write(f"Name: {student_id.name}\n")
        file.write(f"Marks: {student_id.marks}\n")
        file.write(f"Class: {student_id.class_name}\n")
        file.write(f"Roll No: {student_id.roll_no}\n")
        file.write(f"Grade: {student_id.calculate_grade()}\n\n")
    i+= 1
    cont = input("Do you want to enter details for another student? (yes/no): ")
    if cont.lower() != "yes":
        break


