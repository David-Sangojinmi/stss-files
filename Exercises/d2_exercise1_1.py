nthTerm = int(input("What is the nth term: "))
fibList = [0, 1]

def fibonacci(nthTerm):
    if nthTerm == 0:
        return 0
    elif nthTerm == 1:
        return 1   
    else:
        return fibonacci(nthTerm-1) + fibonacci(nthTerm-2)
    
for i in range(2, nthTerm):
    fibList.append(fibonacci(i-1) + fibonacci(i-2))
    
print(fibList)