# Simple Data Validation Engine in Python

def validate_email(email):
    # Check if email contains '@' and '.'
    if "@" in email and "." in email and " " not in email:
        return True
    return False


def validate_phone(phone):
    # Check if phone number has exactly 10 digits
    if phone.isdigit() and len(phone) == 10:
        return True
    return False


def validate_password(password):
    # Check password length and at least one digit
    if len(password) >= 8:
        has_digit = False
        special_chars = "@#$%&"
        for ch in password:
            if ch.isdigit():
                has_digit = True
            if ch in special_chars:
                return True
    return False


# Taking input from user
email = input("Enter email: ")
phone = input("Enter phone number: ")
print("password must carry at least 1 digit and minimum length is 8")
password = input("Enter password: ")

# Validation results
print("\nValidation Results:")
print("Email Valid:", validate_email(email))
print("Phone Valid:", validate_phone(phone))
print("Password Valid:", validate_password(password))
