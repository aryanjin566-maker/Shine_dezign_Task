# Math utility using functions (prime, gcd, lcm, factorial)
def is_prime(num):
  if num <= 1:
    return False
  for i in range(2,num):
    if (num % i) == 0:
      return False
  return True

def gcd(a,b):
  while b != 0:
    a,b = b , a%b
  return a

def lcm(a,b):
  return (a * b) // gcd(a,b)

def factorial(n):
  if n < 0:
    return "Error: Factorial is not defined for negative numbers"
  elif n == 0 or n == 1:
    return 1
  else:
    result = 1
    for i in range(2, n + 1):
      result *= i
    return result
  
#example

print("Is 7 prime?", is_prime(7))
print("GCD of 12 and 18:", gcd(12, 18))
print("LCM of 12 and 18:", lcm(12, 18))
print("Factorial of 5:", factorial(5))
