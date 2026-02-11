import json

# WRITE
data = {
    "name": "Aryan",
    "age": 20,
    "course": "BCA"
}

with open("student.json", "w") as file:
    json.dump(data, file, indent=4)

print("SUCCESFULL.")


# READ
with open("student.json", "r") as file:
    data = json.load(file)

print("Data read from file:")
print(data)


# UPDATE
data["age"] = 21   # Updating age

with open("student.json", "w") as file:
    json.dump(data, file, indent=4)

print("successfully")
