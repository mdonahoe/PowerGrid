


class PowerPlant(object):
    def __init__(self,price,capacity,accepts,rate):
        self.capacity = capacity
        self.price = price
        self.rate = rate
        self.store = dict([(r,0) for r in accepts.split('/')])
    def stock(self, resources):
        assert(len(resources)+sum(self.store.values()) <= self.rate*2)
        for r in resources:
            self._add_resource(r)
    def can_add_resource(self,r):
        return (r in self.store and sum(self.store.values())+1 <= self.rate*2)
    def _add_resource(self,r):
        assert(self.can_add_resource(r))
        self.store[r] += 1
        return self.store[r]
    def _remove_resource(self, r):
        assert(self.store[r] > 0)
        self.store[r] -= 1
        return self.store[r]
    def consume(self,rs):
        assert(self.can_power())
        for _ in range(self.rate):
            self._remove_resource(rs.pop())
    def can_power(self):
        return sum(self.store.values()) >= self.rate
    def obvious_power(self):
        #does this only have one available resource type
        if len(self.store) == 1: return True
        if len(k for k,v in self.store.iteritems() if v)==1: return True
        return False
    def __str__(self):
        rs = ' and '.join('%s %s' % (v,k) for k,v in self.store.iteritems())
        return '$%s %s %s/%s with %s' % (self.price, '/'.join(self.store.keys()), self.rate, self.capacity, rs)


