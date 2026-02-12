filename = "contacts.txt"

def add_contact():
    name = input("Enter contact name: ")
    phone = input("Enter phone number: ")

    with open(filename , "a")as file:
        file.write(f"{name},{phone}\n")
    print("Contact added successfully!")

def view_contacts():
    try: 
        with open(filename , "r") as file:
            print("\n contact details:")
            for line in file:
                name , phone = line.strip().split(",")
                print(f"Name: {name}, Phone: {phone}")
    except FileNotFoundError:
        print("No contacts found. Please add contacts.")

def search_contact():
    serach_name = input("Enter name to search: ")
    found = False
    try:
        with open (filename , "r") as file:
            for line in filename:
                name , phone = line.strip().split(",")
                if name == serach_name:
                    print(f"Found: Name: {name}, Phone: {phone}")
                    found = True
        if not found:
            print("Contact not found!")
    except FileNotFoundError:
        print("No contacts found. Please add contacts.")

def delete_contact():
    delete_name = input("Enter name to delete: ")
    found = False
    data = []

    try:
        with open (filename , "r") as file:
            for line in file:
                name , phone = line.strip().split(",")
                if name != delete_name:
                    data.append(line)
                else:
                    found = True

        with open (filename , "w") as file:
            file.writelines(data)

        if found:
            print("Contact deleted successfully!")
        else:
            print("Contact not found!")
    except FileNotFoundError:
        print("No contacts found. Please add contacts.")

while True:
    print("\nContact Management System")
    print("1. Add Contact")
    print("2. View Contacts")
    print("3. Search Contact")
    print("4. Delete Contact")
    print("5. Exit")

    choice = input("Enter your choice (1-5): ")

    if choice == "1":
        add_contact()
    elif choice == "2":
        view_contacts()
    elif choice == "3":
        search_contact()
    elif choice == "4":
        delete_contact()
    elif choice == "5":
        print("Exiting the system.")
        break
    else:
        print("Invalid choice. Please try again.")