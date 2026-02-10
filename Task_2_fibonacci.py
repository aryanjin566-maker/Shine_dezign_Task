def fibonacci(n):
    if n == 0:        # base case 1
        return 0
    elif n == 1:      # base case 2
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

# printing first 10 Fibonacci numbers
for i in range(5):
    print(fibonacci(i), end=" ")
