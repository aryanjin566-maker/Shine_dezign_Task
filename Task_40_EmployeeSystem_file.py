class employee:
    def __init__(self, name, emp_id, department , salary):
        self.name = name
        self.emp_id = emp_id
        self.department = department
        self.salary = salary
    def display_details(self):
        print(f"Name: {self.name}")
        print(f"Employee ID: {self.emp_id}")
        print(f"Department: {self.department}")
        print(f"Salary: {self.salary}")
    def save_to_file(self, filename):
        with open(filename,"w") as file:
            file.write(f"name : {self.name}\n")
            file.write(f"employee_id : {self.emp_id}\n")
            file.write(f"department : {self.department}\n")
            file.write(f"salary : {self.salary}\n")
    def search_employee(self, emp_id):
        if self.emp_id == emp_id:
            print("Employee found:")
            self.display_details()
            return True
        return False
    def update_employee(self):
        self.name = input("Enter new name: ")
        self.department = input("Enter new department: ")
        self.salary = input("Enter new salary: ")
        print("Employee details updated successfully!")
    def delete_employee(self):
        self.name = ""
        self.emp_id = ""
        self.department = ""
        self.salary = ""
        print("Employee details deleted successfully!")
# Main program
filename = "employee_details.txt"
while True:
    print("\nEmployee Management System")
    print("1. Add Employee")
    print("2. Display Employee Details")
    print("3. Search Employee")
    print("4. Update Employee Details")
    print("5. Delete Employee Details")
    print("6. Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        name = input("Enter employee name: ")
        emp_id = input("Enter employee ID: ")
        department = input("Enter department: ")
        salary = input("Enter salary: ")
        emp = employee(name, emp_id, department)
        emp.save_to_file(filename)
        print("Employee added successfully!")
    elif choice == "2":
        with open(filename, "r") as file:
            content = file.read()
            if content:
                print(content)
            else:
                print("No employee details available.")
    elif choice == "3":
        emp_id = input("Enter employee ID to search: ")
        with open(filename, "r") as file:
            lines = file.readlines()
            found = False
            for line in lines:
                if f"employee_id : {emp_id}" in line:
                    found = True
                    break
            if found:
                with open(filename, "r") as file:
                    content = file.read()
                    print(content)
            else:
                print(f"Employee with ID {emp_id} not found.")
    elif choice == "4":
        emp_id = input("Enter employee ID to update: ")
        with open(filename, "r") as file:
            lines = file.readlines()
            updated_lines = []
            found = False
            for line in lines:
                if f"employee_id : {emp_id}" in line:
                    found = True
                    updated_lines.append(f"name : {input('Enter new name: ')}\n")
                    updated_lines.append(f"employee_id : {emp_id}\n")
                    updated_lines.append(f"department : {input('Enter new department: ')}\n")
                    updated_lines.append(f"salary : {input('Enter new salary: ')}\n")
                else:
                    updated_lines.append(line)
        if not found:
            print(f"Employee with ID {emp_id} not found.")
        else:
            with open(filename, "w") as file:
                file.writelines(updated_lines)
            print("Employee details updated successfully!")
    elif choice == "5":
        emp_id = input("Enter employee ID to delete: ")
        with open(filename, "r") as file:
            lines = file.readlines()
            updated_lines = []
            found = False
            for line in lines:
                if f"employee_id : {emp_id}" in line:
                    found = True
                else:
                    updated_lines.append(line)
        if not found:
            print(f"Employee with ID {emp_id} not found.")
        else:
            with open(filename, "w") as file:
                file.writelines(updated_lines)
            print("Employee details deleted successfully!")
    elif choice == "6":
        break
    else:
        print("Invalid choice. Please try again.")