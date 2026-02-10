list1 = [1, 2, 3, 4, 5,10,6,7,7]
list2 = [6, 7, 8, 9, 10,1,2,5,6,8,1]

#hard way

merged_list = [] 

for num in list1:
  if num not in merged_list:
    merged_list.append(num)

for num in list2:
  if num not in merged_list:
    merged_list.append(num)

print("Merged List:", merged_list)

#easy way
merged_list = list(set(list1) | set(list2))

  