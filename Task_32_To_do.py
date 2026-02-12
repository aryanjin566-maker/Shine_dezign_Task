To_do_list = []

def add_task(task):
    To_do_list.append(task)
    print("Task added successfully!")

def view_tasks():
    if not To_do_list:
        print("NO task found")
        return
    print("\n To-do List:")
    for idx, task in enumerate(To_do_list, start=1):
        print(f"{idx}. {task}")
        
def delete_task():
    view_tasks()
    if not To_do_list:
        return
    try:
        task_num = int(input("Enter task number to delete: "))
        if 1 <= task_num <= len(To_do_list):
            deleted_task = To_do_list.pop(task_num - 1)
            print(f"Task '{deleted_task}' deleted successfully!")
        else:
            print("Invalid task number!")
    except ValueError:
        print("Please enter a valid number!")
  
while True:
    print("\nTo-do List Management")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Delete Task")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        task = input("Enter task description: ")
        add_task(task)
    elif choice == "2":
        view_tasks()
    elif choice == "3":
        delete_task()
    elif choice == "4":
        print("Exiting program. Goodbye!")
        break
    else:
        print("Invalid choice! Please try again.")