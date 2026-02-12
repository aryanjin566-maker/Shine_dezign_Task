user_data = {
   "aryan": "aryan123",
   "riya": "riya123",
   "ram": "ram123"
}

def login(username, password):
    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        if username in user_data and user_data[username] == password:
            print("Login successful!")
            return True
        else:
            attempts += 1
            print(f"login Failed)")
            print (f"you have {max_attempts - attempts} attempts left")
          

    if attempts == max_attempts:
        print("Maximum login attempts reached. Account locked.")
        return False
  
username = input("Enter username: ")
password = input("Enter password: ")
login(username, password)



