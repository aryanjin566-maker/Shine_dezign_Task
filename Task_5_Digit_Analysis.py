#Digit analysis (count, sum, max, min, reverse)

arr  = [123, 456, 789, 10, 11 , 55 , 78 ,63 , 789, 0]

# Count total number in array 
def count(arr):
    return len(arr)

# Sum of all numbers in array
def sum(arr):
    total = 0
    for i in arr:
        total = total + i
    return total


# Max number in array
def max(arr):
    if len(arr) == 0:
        return None
    maximum = arr[0]
    for i in range(1, len(arr)):
        if arr[i] > maximum:
            maximum = arr[i]
    return maximum

# Min number in array

def min(arr):
    if len(arr) == 0:
        return None
    minimum = arr[0]
    for num in arr:
        if num < minimum:
            minimum = num
    return minimum

# Reverse the array
def reverse(arr):
    start = 0 
    end = len(arr) - 1
    while start < end:
     temp = arr[start]
     arr[start] = arr[end]
     arr[end] = temp
     start += 1
     end -= 1
    print("Reversed array:", arr)


print("Count:", count(arr))
print("Sum:", sum(arr))
print("Max:", max(arr))
print("Min:", min(arr))
reverse(arr)




      
      
