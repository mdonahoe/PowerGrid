"""resource market"""
import math
import random

import constants
import powerplant


class SupplyError(Exception):
    pass


class PowerPlantMarket(object):
    def __init__(self):
        ps = [powerplant.PowerPlant(*args) for args in constants.powerplants]
        special = ps.pop(10)
        self.deck = ps[8:]
        random.shuffle(self.deck)
        self.deck = [special] + self.deck[8:]
        self.visible = ps[:8]

    def draw(self):
        p = self.deck.pop(0)
        self.visible.append(p)
        self.visible.sort(lambda a, b: cmp(a.price, b.price))
        assert(len(self.visible) == 8)

    def actual(self):
        return self.visible[:4]

    def future(self):
        return self.visible[4:8]

    def buy(self, powerplant):
        assert(powerplant in self.actual())
        self.visible.remove(powerplant)
        self.draw()

    def cycle_deck(self):
        self.deck.append(self.visible.pop())
        self.draw()


class ResourceSubMarket(object):
    def __init__(self, resource, initial_supply, bucket_size, bucket_prices, step_vars):
        self.resource = resource
        self.supply = initial_supply
        self.total = bucket_size * len(bucket_prices)
        self.available = self.total - initial_supply
        self.bucket_size = bucket_size
        self.bucket_prices = bucket_prices
        self.step_vars = step_vars

    def __str__(self):
        return '$%s/%s' % (self.current_price(), self.resource)

    @property
    def resupply_rate(self):
        return self.step_vars.get_resupply_rate(self.resource)

    def current_price(self, supply=None):
        if supply is None:
            supply = self.supply
        assert(supply >= 0)
        if supply == 0:
            raise SupplyError()
        b = -int(math.ceil(1.0 * supply / self.bucket_size))
        return self.bucket_prices[b]

    def price_for_n(self, n):
        if n > self.supply:
            raise SupplyError()
        return sum(self.current_price(self.supply - i) for i in range(n))

    def resupply(self):
        resupply = min(self.resupply_rate, self.available)
        self.available -= resupply
        self.supply += resupply
        assert(self.available >= 0)
        assert(self.supply + self.available <= self.total)

    def buy(self, n):
        cost = self.price_for_n(n)
        self.supply -= n
        assert(self.supply >= 0)
        return cost

    def restock(self, n):
        self.available += n
        assert(self.available + self.supply <= self.total)


if __name__ == '__main__':
    import constants
    import step_vars
    sv = step_vars.StepVars(2)
    oil = ResourceSubMarket('oil', 10, 3, range(1, 9), sv)
    assert(oil.price_for_n(4) == 23)
    print "Tests have passed"
