string1 = "hello"
string2 = "oellwh"

def are_anagrams(str1, str2):
    # Remove spaces and convert to lowercase
    str1 = str1.replace(" ","").lower()
    str2 = str2.replace(" ","").lower()
    
    # Sort the characters of both strings and compare
    return sorted(str1) == sorted(str2)


if are_anagrams(string1, string2):
    print(f"'{string1}' and '{string2}' are anagrams.")
else:
    print(f"'{string1}' and '{string2}' are not anagrams.")


# fastest way to check anagram is to use collections module

from collections import Counter

s1 = "programming"
s2 = "mmogginparr"

counter1 = Counter(s1)
counter2 = Counter(s2)

if counter1 == counter2:
    print("The strings have matching character frequencies.")
else:
    print("The strings do not have matching character frequencies.")
