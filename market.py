"""resource market"""
import math
import random

import constants
import powerplant


class SupplyError(Exception):
    pass


class PowerPlantMarket(object):
    def __init__(self, step_vars):
        self.step_vars = step_vars
        ps = [powerplant.PowerPlant(*args) for args in constants.powerplants]
        # Grab the $13 Eco plant
        special = ps.pop(10)
        # Remove the first 8 cards and shuffle the rest
        self.deck = ps[8:]
        self.shuffle()
        # Remove the top few cards
        self.deck = self.deck[step_vars.power_plants_to_remove:]
        # Put the $13 eco plant on top
        self.deck.insert(0, special)

        self.step3 = powerplant.PowerPlant(999, 0, 'eco', 1)
        self.deck.append(self.step3)
        # create the visible market
        self.visible = ps[:8]

        self._did_step3_shuffle = False
    def discard_low_power_plants(self, players):
        most_cities = max(len(player.cities) for player in players)
        while self.visible:
            if self.visible[0].price <= most_cities:
                self.visible.pop(0)
                self.draw()
            else:
                break

    def draw(self):
        if len(self.deck) == 0:
            return
        p = self.deck.pop(0)
        if p == self.step3:
            self.shuffle(step3=True)
        self.visible.append(p)
        self.visible.sort()
        assert len(self.visible) <= 8
        if self.deck and self.step_vars.step < 3:
            # Not true in step 3
            assert len(self.visible) == 8

    def actual(self):
        if self.step_vars.step < 3:
            return self.visible[:4]
        else:
            return self.visible

    def future(self):
        assert self.step_vars.step < 3, "no future market in step 3"
        return self.visible[4:8]

    def buy(self, powerplant):
        assert powerplant in self.actual(), "that powerplant is not for sale"
        self.visible.remove(powerplant)
        self.draw()

    def shuffle(self, step3=False):
        self._did_step3_shuffle = True
        random.shuffle(self.deck)

    def discard_lowest(self):
        if self.visible:
            self.visible.pop(0)
        self.draw()

    def cycle_deck(self):
        if self.step_vars.step == 3:
            if self.visible:
                self.visible.pop(0)
        else:
            # Remove the highest priced visible powerplant
            # and put it at the bottom of the deck
            self.deck.append(self.visible.pop())
        self.draw()

    def do_step_three(self):
        print 'STEP THREE'
        self.step_vars.step = 3
        if self.step3 in self.visible:
            self.visible.remove(self.step3)
        if self.visible:
            self.visible.pop(0)
        assert len(self.visible) <= 6
        if not self._did_step3_shuffle:
            self.shuffle()


class ResourceSubMarket(object):
    def __init__(self, step_vars, resource, initial_supply, bucket_size, bucket_prices):
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
        assert supply >= 0
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
        print 'restocking %s %s' % (resupply, self.resource)
        self.available -= resupply
        self.supply += resupply
        assert self.available >= 0
        assert self.supply + self.available <= self.total

    def buy(self, n):
        cost = self.price_for_n(n)
        self.supply -= n
        assert self.supply >= 0
        return cost

    def restock(self, n):
        self.available += n
        assert self.available + self.supply <= self.total

