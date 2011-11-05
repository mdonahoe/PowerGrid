class PowerPlant(object):
    """Power plants create energy to power cities.
    Each one consumes a type of resource,
    and produces an amount of energy.
    It also has a starting bid price."""
    def __init__(self, price, capacity, accepts, rate):
        self.capacity = capacity # number of cities it can power
        self.price = price # starting price for this powerplant
        self.rate = rate # number of resources required to power it
        self.store = dict((r, 0) for r in accepts.split('/')) # current resource allotment

    def stock(self, resources):
        """A resources to this power plant"""
        assert sum(resources.values()) + sum(self.store.values()) <= self.rate * 2
        for r, count in resources.iteritems():
            self._add_resource(r, count)

    def better_stock(self, rs):
        """Stock as many resources from a dictionary as possible, return remaining"""
        for r in rs:
            if not rs[r] or r not in self.store:
                continue
            while rs[r] and self.can_add_resource(r, 1):
                self._add_resource(r, 1)
                rs[r] -= 1
        return dict((r, c) for r, c in rs.iteritems() if c)

    def can_add_resource(self, r, count):
        """This plant accepts a certain type of resource
        and can't fit more than 2 times its consumption rate"""
        return (r in self.store
                and sum(self.store.values()) + count <= self.rate * 2)

    def _add_resource(self, r, count):
        assert(self.can_add_resource(r, count))
        self.store[r] += count
        return self.store[r]

    def _remove_resource(self, r, count):
        assert self.store[r] >= count
        self.store[r] -= count
        return self.store[r]

    def consume(self, rs):
        assert self.can_power()
        assert sum(rs.values()) == self.rate
        for r, count in rs.iteritems():
            self._remove_resource(r, count)

    def can_power(self):
        return sum(self.store.values()) >= self.rate

    def obvious_power(self):
        #does this only have one available resource type
        if len(self.store) == 1: return True
        if len(k for k, v in self.store.iteritems() if v)==1: return True
        return False

    def resources_needed(self):
        return self.rate - sum(self.store.values())

    @property
    def hybrid(self):
        return len(self.store.keys()) > 1

    def __cmp__(self, other):
        return cmp(self.price, other.price)

    def __str__(self):
        rs = ' and '.join('%s %s' % (v, k) for k, v in self.store.iteritems())
        return '$%s %s %s/%s with %s' % (self.price, '/'.join(self.store.keys()), self.rate, self.capacity, rs)

    def __repr__(self): return str(self)
