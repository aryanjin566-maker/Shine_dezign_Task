nested_list = [
    ["name", "Aryan"],
    ["age", 20],
    ["course", "BCA"]
]

dictionary = {}

for i in range(len(nested_list)):
    key  = nested_list[i][0]
    value = nested_list[i][1]
    dictionary[key] = value

print(dictionary)


#easy way to convert nested list to dict
# result = dict(nested_list)
# print(result)