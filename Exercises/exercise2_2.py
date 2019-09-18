noOfNumbers = int(input("How many numbers are you inputting? "))
numbers = []
i = 0
maxNumber = 0

for i in range(1, noOfNumbers+1):
    numbers.append(input("Enter your number: "))

maxNumber = numbers[0]

for i in range(1, noOfNumbers):
    if numbers[i] > maxNumber:
        maxNumber = numbers[i]

print(maxNumber)
