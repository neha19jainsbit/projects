import math

# number = int(input("Enter a non-negative integer: "))
# if number < 0:
#     print("Factorial is not defined for negative numbers")
# else:
#     print("Factorial of", number, "is", math.factorial(number))

# n= 0.4  
# x = 4
# result = n ** x
# print(result)


from scipy.stats import binom

# Given values
n = 10
p = 0.25
k = 2

# Calculate the probability that at most 4 people show up
#probability = binom.cdf(k, n, p)
probability = binom.pmf(k, n, p)

print(probability)
