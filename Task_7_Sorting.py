arr = [64, 34, 25, 12, 22, 11, 90]
t=1
for i in range(len(arr)):
    t += 1
    print(t)
    for j in range(i+1 , len(arr)):
        t += 1
        if arr[i] > arr [j]:
            temp = arr[i]
            arr[i] = arr[j]
            arr[j] = temp

print("Sorted array:", arr)