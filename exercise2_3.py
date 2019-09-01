x = int(input("Number: "))
n = int(input("Power: "))
numVal = x

for i in range(1, n):
    numVal = numVal*x
    
print(numVal)