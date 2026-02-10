arr = [64, 34, 25, 12, 22, 11, 90]

for i in range(len(arr)):
    for j in range(i+1 , len(arr)):
        if arr[i] > arr [j]:
            temp = arr[i]
            arr[i] = arr[j]
            arr[j] = temp

print("Sorted array:", arr)

# Find second largest and second smallest elements
if len(arr) < 2:
    print("Array should have at least two elements.")
else:
    second_largest = arr[-2]
    second_smallest = arr[1]
    print("Second Largest:", second_largest)
    print("Second Smallest:", second_smallest)