#Leaner Search
def linear_search(arr,key):
    for i in range(len(arr)):
        if  arr[i] == key:
            return i
    return -1

#Binary Search
def binary_search(arr, key):
    start = 0
    end = len(arr) - 1
    while start <= end:
        mid = start + (end - start) // 2 # it does not crack at max value of int
        if arr[mid] == key:
            return mid
        elif arr[mid] < key:
            start = mid + 1
        else:
            end = mid - 1
    return -1

# Example usage
arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
key = 5
print("Linear Search: Key found at index:", linear_search(arr, key))
print("Binary Search: Key found at index:", binary_search(arr, key))