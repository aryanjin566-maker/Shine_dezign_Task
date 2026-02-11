# Check if the number is an Armstrong number
number = int (input("Enter a number: "))
def is_armstrong(num):
    sum = 0 
    temp = num
    while temp > 0 :
        digit = temp % 10
        sum += digit** (len(str(num)))
        temp = temp // 10 
        return sum 
    
if number == is_armstrong(number):
    print(number, "is an Armstrong number")
else:
    print(number, "is not an Armstrong number")


# Check if the number is a palindrome

def is_palindrome(num):
    return str(num) == str(num)[::-1]

number = int (input("Enter a number: "))
palindrome = is_palindrome(number)

if palindrome:
    print(number, "is a palindrome")
else:
    print(number, "is not a palindrome")


# Check if the number is a perfect number

number = int (input("Enter a number: "))
def is_perfect(num):
    sum = 0 
    for  i  in range (1,num):
        if num %  i == 0:
            sum += i
    return sum == num

if is_perfect(number):
    print(number, "is a perfect number")
else:
    print(number, "is not a perfect number")
