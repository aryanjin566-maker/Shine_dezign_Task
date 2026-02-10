#for loop
def factorial(number):
    
    if number < 0 : 
        print ("Enter Positive number")
        return None
    
    if number == 0 or  number == 1 :
        return 1 
    
    result = 1 ; 
    for i in range (1,number+1):
       result = result * i
    return result

#recussion

def factorial_recursive(number):
    
    if number < 0 : 
        print ("Enter Positive number")
        return None
    
    if number == 0 or  number == 1 :
        return 1 
    
    else:
        return number * factorial_recursive(number - 1)

