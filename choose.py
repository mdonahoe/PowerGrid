def choose(xs,k,r=False):
    if k==0: return []
    choices = []
    while xs:
        x = xs.pop(0)
        cs = choose(r and [x]+xs or xs[:],k-1,r)
        if cs:
            choices.extend([x]+c for c in cs)
        elif k==1:
            choices.append([x])
    return choices

def bits(n):
    """Returns a list of bits"""
    bs = []
    while n > 0:
        bs.append(n%2)
        n = int(n/2)
    return bs

def all_subsets(xs):
    if not xs: yield []
    items = list(xs)
    n = len(items)
    for i in xrange(2**n):
        yield [item for item, bit in zip(items, bits(i)) if bit]

def all_subsets(items):
    """iterates through all the "subsets" of a given iterable, including the empty set"""
    items = tuple(items)
    for n in xrange(2**len(items)):
        subset = []
        i = 0
        while n:
            if n % 2:
                subset.append(items[i])
            i += 1
            n = int(n / 2)
        yield tuple(subset)



if __name__=='__main__':
    # tests!
    print choose(range(3),2)
    print choose(range(3),2,1)
    assert choose([1,2,3],1) == [[1],[2],[3]]
    assert choose([1,2,3],2) == [[1,2],[1,3],[2,3]]
    assert len(choose(range(6),2)) == 15
    assert choose([1,2],2,True) == [[1,1],[1,2],[2,2]]
