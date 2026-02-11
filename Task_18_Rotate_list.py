my_list = [1, 2, 3, 4, 5]
k = 3

def right_rotate_list(lst, k):
    k = k % len(lst) 
    return lst[-k:] + lst[:-k]
rotated_list = right_rotate_list(my_list, k)
print("Original list:", my_list)
print("Rotated list:", rotated_list)


def left_rotate_list(lst, k):
    k = k % len(lst) 
    return lst[k:] + lst[:k]
rotated_list = left_rotate_list(my_list, k)
print("Original list:", my_list)
print("Rotated list:", rotated_list)