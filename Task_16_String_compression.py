string1 = input("Enter the string: ")

def frequent_character(word):
    frequency  = {}
    for char in word:
        if char in frequency:
            frequency[char] += 1 
        else:
            frequency[char] = 1 
    return frequency 

string_compression = frequent_character(string1)
for key , value in string_compression.items():
    print(f"{key}{value}", end="")
