

zeroArray = [0,0,0,0,0,0]


def getSplits(startArray,endArray):
    results = []
    if(len(startArray) == 6):
        sA = startArray
    else:
        print("To little points given to getSplits in moveSplitter.py")
        print("going home")
        results.append(zeroArray)
        return results
    if(len(endArray) == 6):
        eA = endArray
    else:
        print("To little points given to getSplits in moveSplitter.py")
        print("going home")
        results.append(zeroArray)
        return results
    diffArray = []
    for x in range(6):
        diffArray.append(float(eA[x])-float(sA[x]))
    
    totalMove = 0
    for point in diffArray:
        totalMove+=point
    print("Total Move: " + str(totalMove)+ " radians")
    steps = totalMove*2
    for x in range(6):
        diffArray[x]=diffArray[x]/steps
    
    for i in range(int(steps)):
        for x in range(6):
            sA[x] = sA[x] + diffArray[x]
        results.append(sA)
        
    return results