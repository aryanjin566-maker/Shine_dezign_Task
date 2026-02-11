# Reverse words in a sentence without changing word order
sentence = "olleH nayrA"
word = sentence.split()
reversed_word = []
for i in word:
   reversed_word.append(i[::-1])
reversed_sentence = " ".join(reversed_word)
print(f"'{reversed_sentence}'")