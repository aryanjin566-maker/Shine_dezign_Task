word = str(input("Enter a word: ")) 
def most_frequent_character(word):
    frequency  = {}
    for char in word:
        if char in frequency:
            frequency[char] += 1 
        else:
            frequency[char] = 1 
        
    most_frequent_character = max(frequency, key= frequency.get)
    return most_frequent_character

result = most_frequent_character(word)
print("Most frequent character:", result)