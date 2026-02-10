string1= "Programming"

def remove_duplicates(string):
    result = ""
    for char in string1:
        if char not in result:
            result += char
    return result