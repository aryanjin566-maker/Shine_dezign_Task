# Use lambda, map, filter, reduce for transformations
from functools import reduce

number = [1, 2, 3, 4, 5]
# map
sqaure = list(map(lambda x: x*x, number))
# filter
even_sqaure = list(filter(lambda x:x%2 == 0 , sqaure))
# reduce
sum_of_sqaure = reduce(lambda x,y: x+y, sqaure)

print("Square of numbers:", sqaure)
print("Even squares:", even_sqaure)
print("Sum of squares:", sum_of_sqaure)
