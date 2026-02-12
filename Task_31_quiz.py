score = 0 ; 
print("Welcome to the Quiz!")

for i in range(1, 6):
    print(f"Question {i} :")
    if i == 1 :
        answer = input("What is the capital of France?\n a) Berlin \n b) Madrid \n c) Paris \n d) Rome\n Your answer: ")
        if answer.lower() == 'c':
            score += 1
            print("Correct!")
        else:
            print("Wrong! The correct answer is c) Paris.")
    elif i == 2 :
        answer = input("What is 125 * 125 ?\n a) 15623 \n b) 15625 \n c) 15620 \n d) 15606\n Your answer: ")
        if answer.lower() == 'b':
            score += 1
            print("Correct!")
        else:
            print("Wrong! The correct answer is b) 15625.")
    elif i == 3 :
        answer = input("What is the largest planet in our solar system?\n a) Earth \n b) Mars \n c) Jupiter \n d) Saturn\n Your answer: ")
        if answer.lower() == 'c':
            score += 1
            print("Correct!")
        else:
            print("Wrong! The correct answer is c) Jupiter.")
    elif i == 4 :
        answer = input("Who wrote 'Romeo and Juliet'?\n a) Charles Dickens \n b) William Shakespeare \n c) Mark Twain \n d) Jane Austen\n Your answer: ")
        if answer.lower() == 'b':
            score += 1
            print("Correct!")
        else:
            print("Wrong! The correct answer is b) William Shakespeare.")
    elif i == 5 : 
        answer = input("What is the chemical symbol for water?\n a) CO2 \n b) H2O \n c) O2 \n d) NaCl\n Your answer: ")
        if answer.lower() == 'b':
            score += 1
            print("Correct!")
        else:
            print("Wrong! The correct answer is b) H2O.")
print(f"\nQuiz Over! Your total score is: {score} out of 5.")