class Employee:
    # Constructor to initialize employee details
    def __init__(self, emp_id, name, department, salary):
        self.emp_id = emp_id
        self.name = name
        self.department = department
        self.salary = salary

    # Method to display employee details
    def display(self):
        print("\nEmployee Details:")
        print("ID:", self.emp_id)
        print("Name:", self.name)
        print("Department:", self.department)
        print("Salary:", self.salary)


class EmployeeManagementSystem:
    def __init__(self):
        # Dictionary to store employees (In-Memory)
        # Key = emp_id, Value = Employee object
        self.employees = {}

    # Add new employee
    def add_employee(self):
        emp_id = input("Enter Employee ID: ")

        if emp_id in self.employees:
            print("Employee ID already exists!")
            return

        name = input("Enter Name: ")
        department = input("Enter Department: ")
        salary = float(input("Enter Salary: "))

        emp = Employee(emp_id, name, department, salary)
        self.employees[emp_id] = emp

        print("Employee added successfully!")

    # View all employees
    def view_all_employees(self):
        if not self.employees:
            print("No employees found.")
            return

        for emp in self.employees.values():
            emp.display()

    # Search employee by ID
    def search_employee(self):
        emp_id = input("Enter Employee ID to search: ")

        if emp_id in self.employees:
            self.employees[emp_id].display()
        else:
            print("Employee not found!")

    # Update employee salary
    def update_salary(self):
        emp_id = input("Enter Employee ID to update salary: ")

        if emp_id in self.employees:
            new_salary = float(input("Enter New Salary: "))
            self.employees[emp_id].salary = new_salary
            print("Salary updated successfully!")
        else:
            print("Employee not found!")

    # Delete employee
    def delete_employee(self):
        emp_id = input("Enter Employee ID to delete: ")

        if emp_id in self.employees:
            del self.employees[emp_id]
            print("Employee deleted successfully!")
        else:
            print("Employee not found!")


# ===== Main Program =====

system = EmployeeManagementSystem()

while True:
    print("\n===== Employee Management System =====")
    print("1. Add Employee")
    print("2. View All Employees")
    print("3. Search Employee")
    print("4. Update Salary")
    print("5. Delete Employee")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        system.add_employee()

    elif choice == "2":
        system.view_all_employees()

    elif choice == "3":
        system.search_employee()

    elif choice == "4":
        system.update_salary()

    elif choice == "5":
        system.delete_employee()

    elif choice == "6":
        print("Exiting system...")
        break

    else:
        print("Invalid choice! Try again.")
