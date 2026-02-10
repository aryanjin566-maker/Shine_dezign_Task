
numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10]

for num in numbers :
  if num > 1 :

    Prime = True 

    for i in range (2,num):
      if (num % i) == 0 :
        Prime = False
        break
      
    if Prime:
      print(num)

  else:
    print(num, "is not a prime number")