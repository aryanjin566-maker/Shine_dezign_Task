filename = "students.txt"

print("1. Add")
print("2. Search")
print("3. Delete")

choice = input("Enter choice: ")

# ---------- ADD ----------
if choice == "1":
    name = input("Enter name: ")
    marks = input("Enter marks: ")

    with open(filename, "a") as f:
        f.write(name + "," + marks + "\n")

    print("Record added!")


# ---------- SEARCH ----------
elif choice == "2":
    name_to_search = input("Enter name to search: ")
    found = False

    with open(filename, "r") as f:
        for line in f:
            name, marks = line.strip().split(",")
            if name == name_to_search:
                print("Found:", name, marks)
                found = True

    if not found:
        print("Name not found!")


# ---------- DELETE ----------
elif choice == "3":
    name_to_delete = input("Enter name to delete: ")
    found = False
    data = []

    with open(filename, "r") as f:
        for line in f:
            name, marks = line.strip().split(",")
            if name != name_to_delete:
                data.append(line)
            else:
                found = True

    with open(filename, "w") as f:
        f.writelines(data)

    if found:
        print("Record deleted!")
    else:
        print("Name not found!")


else:
    print("Invalid choice")
