class invalidInputError(Exception):
    pass

def check_number(num):
    if num < 0:
        raise invalidInputError("Negative numbers are not allowed")
    else:
       print(f"The number {num} is valid")


try:
    number = int(input("Enter a number: "))
    check_number(number)

except invalidInputError as e:
    print(e)

except ValueError:
    print("Invalid input. Please enter a valid integer.")

finally:
    print("Program ended.")
    