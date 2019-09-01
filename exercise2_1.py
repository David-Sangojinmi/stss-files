def evens(k):
    evenNumbers = []
    kK = k + 1
    
    for i in range(0, kK):
        if (i%2) == 0:
            evenNumbers.append(i)
        
    print(evenNumbers)

k = int(input("What is your target number? "))
evens(k)
