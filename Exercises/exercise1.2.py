startValue = input("What are you depositing? ")
months = int(input("How many months are you keeping your money for? "))
currentValue = startValue
nextValue = 0

for i in range(1, months):
    nextValue = currentValue * 1.01
    currentValue = nextValue
    print("You now have: " + currentValue + ".")
