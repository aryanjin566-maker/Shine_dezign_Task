# Global variables

balance = 0
transactions = []

# Function to deposit money

def deposit(amount):
    global balance
    if amount > 0:
        balance += amount
        transactions.append(f"Deposited: {amount}")
        print("Money deposited successfully.")
    else:
        print("Invalid amount")

# Function to withdraw money

def withdraw(amount):
    global balance
    if amount > balance:
        print("Insufficient balance!")
    elif amount <= 0:
        print("Invalid amount!")
    else:
        balance -= amount
        transactions.append(f"Withdrawn: {amount}")
        print("Money withdrawn successfully.")

# Function to show balance

def show_balance():
    print("Current Balance:", balance)

# Function to show transaction history

def show_transactions():
    print("\nTransaction History:")
    if len(transactions) == 0:
        print("No transactions yet.")
    else:
        for t in transactions:
            print("-", t)


while True:
    print("\n1. Deposit")
    print("2. Withdraw")
    print("3. Show Balance")
    print("4. Show Transactions")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        amount = float(input("Enter amount to deposit: "))
        deposit(amount)

    elif choice == "2":
        amount = float(input("Enter amount to withdraw: "))
        withdraw(amount)

    elif choice == "3":
        show_balance()

    elif choice == "4":
        show_transactions()

    elif choice == "5":
        print("Thank you")
        break

    else:
        print("Invalid choice")

