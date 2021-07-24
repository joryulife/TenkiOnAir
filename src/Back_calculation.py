from typing import Collection


def BackCalculation(CollectionSum):
    Collection = []
    if CollectionSum == 0:
        return Collection
    while CollectionSum > 0:
        i = 0
        while 1 :
            if 2**i > CollectionSum:
                CollectionSum = CollectionSum - 2**(i-1)
                Collection.append(2**(i-1))
                i=0
                break
            elif 2**i == CollectionSum :
                CollectionSum = CollectionSum - 2**i
                Collection.append(2**i)
                i=0
                break
            else:
                i+=1
    
    return Collection
