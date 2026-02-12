# File name
filename = "student_data.txt"

while True:
    print("\n1. Add Student")
    print("2. View Students")
    print("3. Exit")

    choice = input("Enter your choice: ")

    # Add Student (Write / Append)
    if choice == "1":
        name = input("Enter student name: ")
        marks = input("Enter marks: ")

        with open(filename, "a") as file:
            file.write(f"{name},{marks}\n")

        print("Data saved successfully!")

    # View Students (Read)
    elif choice == "2":
       try:
           with open(filename,"r") as file:
               print("\n student details:")
               for line in file:
                   name , marks = line.strip().split(",")
                   print(f"Name: {name},\nMarks: {marks}")
       except FileNotFoundError:
            print("No student data found. Please add students data.")

    # Exit
    elif choice == "3":
        print("Program Ended.")
        break

    else:
        print("Invalid choice!")
