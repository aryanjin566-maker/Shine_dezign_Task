import datetime
class login_data:
    def __init__(self, username, password):
        self.username = username
        self.password = password
  
    def user_details(self):
        with open ("user_details.txt" , "w") as file:
            file.write(f"Login Timestamp: {datetime.datetime.now()}\n") 
            file.write(f"Username: {self.username}\n")
            file.write(f"Password: {self.password}\n")
        print("User details written to file successfully.")

    def login(self):
        with open("user_details.txt", "r") as file:
            stored_username = file.readline().strip().split(": ")[1]
            stored_password = file.readline().strip().split(": ")[1]

        if self.username == stored_username and self.password == stored_password:
            print("Login successful!")
        else:
            print("Login failed. Invalid username or password.") 

username = input("Enter username: ")
password = input("Enter password: ")
user = login_data(username, password)
user.user_details()
user.login()
