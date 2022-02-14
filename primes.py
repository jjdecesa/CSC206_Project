import time

sTime  = time.time()
listOfPrime = []
tempBool = True

high = 0
high = int(input("input upper limit: "))

for all in range(1, high + 1, 2):
    tempBool = True
    #print(all, "a")
    for all2 in range(2, all):
        if (all % all2 == 0):
            tempBool = False
    
    if tempBool:
        listOfPrime.append(all)
            

print("All primes: ", listOfPrime)
print("Time in Seconds: ", time.time() - sTime)