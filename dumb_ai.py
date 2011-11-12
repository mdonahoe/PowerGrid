import player
import market


class DumbAI(player.Player):
    def choose_power_plant_to_discard(self):
        return self.power_plants[0]

    def redistribute_resources(self,rs):
        """move resources to other power plants and return overflow"""
        return rs

    def initial_bid(self, pp_market, bidders):
        """Buy the cheapest, if we can afford it"""
        actual = pp_market.actual()
        if not actual:
            return None
        cheapest = pp_market.actual()[0]
        if cheapest.price <= self.money:
            return cheapest.price, cheapest
        return None

    def get_bid(self, price, plant, bidders):
        """never outbid"""
        return None

    def choose_resources_to_buy(self, resource_market):
        """never buy resources"""
        return None

    def build_cities(self, grid):
        """buy the cheapest city we can afford"""
        cities = grid.price_sorted(self.cities)
        if not cities:
            return
        (price, cheapest) = cities[0]
        cheapest = grid.cities[cheapest]
        if price <= self.money:
            self.buy_city(cheapest, price)

    def power_plants_to_use(self):
        """never power a plant (we havent bought an resources anyway"""
        return []


class BareMinimumAI(DumbAI):
    """
    Does the bare minimum to try to win
    1. Buys one power plant
    2. buys a single city
    3. always powers that city
    """
    def initial_bid(self, pp_market, bidders):
        if self.power_plants:
            return None
        return super(BareMinimumAI, self).initial_bid(pp_market, bidders)

    def choose_resources_to_buy(self, resource_market):
        """Buy enough resources to power our only plant"""
        if not self.power_plants:
            return None
        plant = self.power_plants[0]
        resource = plant.store.keys()[0]
        n = plant.resources_needed()
        if resource == 'eco': return
        m = resource_market[resource]
        resource_market[resource].buy(n)
        plant.stock({resource: n})

    def build_cities(self, grid):
        super(BareMinimumAI, self).build_cities(grid)

    def power_plants_to_use(self):
        """power all our plants... this might use more resources than the plant has"""
        return [(p, {p.store.keys()[0]: p.rate}) for p in self.power_plants if p.store.values()[0] >= p.rate]


class Outbidder(DumbAI):
    """always tries to outbid you"""
    def get_bid(self, price, plant, bidders):
        if price < self.money:
            return price + 1
        return None


class BasicAI(DumbAI):
    """Buys a new power plant, resources, and a city every round"""
    def choose_resources_to_buy(self, resource_market):
        for plant in self.power_plants:
            resource = plant.store.keys()[0]
            n = plant.resources_needed()
            if n == 0: continue
            m = resource_market[resource]
            m.buy(n)
            plant.stock({resource: n})

    def power_plants_to_use(self):
        return [(p, {p.store.keys()[0]: p.rate}) for p in self.power_plants if p.store.values()[0] >= p.rate]


class PowerAI(player.Player):
    """
    Bidding:
        Buy most expensive power plant
        Don't buy hybrids
        In get_bid, bid $1 more than the minimum price...
            if the cheapest powerplant in the future market
            costs that much

    Resources:
        Buy resources to power all power plants, in decreasing order

    Cities:
        Buy as many as you can power
        Greedy on price, name

    Powering:
        Burn as many powerplants as necessary
        Start with eco
        then most expensive

    Reallocation:
        Put as many as you can on the most expensive

    """

    def choose_power_plant_to_discard(self):
        """Always remove the cheapest"""
        return self.power_plants[0]

    def redistribute_resources(self,rs):
        """move resources to other power plants and return overflow"""

        for plant in reversed(self.power_plants):
            rs = plant.better_stock(rs)

        return rs

    def initial_bid(self, pp_market, bidders):
        """Bid on the highest non-hybrid"""
        print 'actual market: ', [plant.price for plant in pp_market.actual()]
        for plant in reversed(pp_market.actual()):
            if plant.hybrid or plant.price > self.money:
                continue
            if len(self.power_plants) == 4 and plant.price < min([x.price for x in self.power_plants]):
                print '%s decides these power plants are too cheap, and passes' % self.name
                return None
            print self.name, 'bids on', plant.price
            return plant.price, plant
        print '%s passed' % self.name
        return None

    def get_bid(self,price,plant,bidders):
        """Bid only when the cheapest future plant
        is the same price as plant.price + 1"""
        if plant.hybrid:
            return 0
        if price != plant.price:
            return 0
        if price >= self.money:
            return 0
        if self.game.step_vars.step == 3:
            return 0
        future = self.game.power_plant_market.future()[0]
        if price + 1 == future.price:
            bid = price + 1
            print '%s outbids with %s' %(self.name, bid)
            return bid
        return 0

    def choose_resources_to_buy(self, resource_market):
        """Buy resources for all powerplants, decreasing"""
        print '%s buying resources' % self.name
        for plant in reversed(self.power_plants):
            n = plant.resources_needed()
            if n <= 0:
                continue
            resource = sorted(plant.store.keys())[0]
            print '\tneed %s %s' % (n, resource)
            if self.buy_resources(resource_market, {resource: n}):
                plant.stock({resource: n})

    def build_cities(self, grid):
        """Buy as many as you can power
        starting with cheapest and alphabetically"""
        print '%s buying cities' % self.name
        while True:
            cities = grid.price_sorted(self.cities)
            #print cities[:2], self.name, self.money
            if not cities:
                #print self.cities
                #print set([city.name for city in self.cities])-set(grid.cities.keys())
                return
            price, name = cities[0]
            city = grid.cities[name]
            if price > self.money or len(self.cities) >= self.total_capacity():
                break
            self.buy_city(city, price)
            print '\t%s for %s' % (name, price)
        print '\t$%s left' % self.money

    def power_plants_to_use(self):
        """
        Power all ecos
        power from most expensive down
        until we can power all cities
        """
        prs = []
        powered = 0
        cities = len(self.cities)
        for plant in self.power_plants:
            if 'eco' in plant.store:
                prs.append((plant, {}))
                powered += plant.capacity
        for plant in reversed(self.power_plants):
            if powered >= cities:
                print self.name, prs
                return prs
            if 'eco' in plant.store:
                continue
            if not plant.can_power():
                continue
            powered += plant.capacity
            prs.append((plant, {plant.store.keys()[0]: plant.rate}))
        print self.name, prs
        return prs

class SuperPowerAI(PowerAI):
    """
    Bidding:
        Buy most expensive power plant, if we are at capacity
        In get_bid, bid $1 more than the minimum price...
            if the cheapest powerplant in the future market
            costs that much

    Resources:
        Buy resources to power all power plants, in decreasing order

    Cities:
        Buy as many as you can power
        Greedy on price, name

    Powering:
        Burn as many powerplants as necessary
        Start with eco
        then most expensive

    Reallocation:
        Put as many as you can on the most expensive

    """

    def initial_bid(self, pp_market, bidders):
        """Bid on the highest non-hybrid"""
        print 'actual market: ', [plant.price for plant in pp_market.actual()]
        if len(self.cities) < self.total_capacity():
            return None
        for plant in reversed(pp_market.actual()):
            if plant.price > self.money:
                continue
            if len(self.power_plants) == 4 and plant.price < min([x.price for x in self.power_plants]):
                print '%s decides these power plants are too cheap, and passes' % self.name
                return None
            print self.name, 'bids on', plant.price
            return plant.price, plant
        print '%s passed' % self.name
        return None

    def get_bid(self,price,plant,bidders):
        """Bid only when the cheapest future plant
        is the same price as plant.price + 1"""
        if len(self.cities) < self.total_capacity():
            return 0
        if price != plant.price:
            return 0
        if price >= self.money:
            return 0
        if self.game.step_vars.step == 3:
            return 0
        future = self.game.power_plant_market.future()[0]
        if price + 1 == future.price:
            bid = price + 1
            print '%s outbids with %s' %(self.name, bid)
            return bid
        return 0

    def power_plants_to_use(self):
        """
        Power all ecos
        power from most expensive down
        until we can power all cities
        """
        prs = []
        powered = 0
        cities = len(self.cities)
        for plant in self.power_plants:
            if 'eco' in plant.store:
                prs.append((plant, {}))
                powered += plant.capacity
        for plant in reversed(self.power_plants):
            if powered >= cities:
                print self.name, prs
                return prs
            if 'eco' in plant.store:
                continue
            if not plant.can_power():
                continue
            powered += plant.capacity
            rs = {}
            for r in sorted(plant.store.keys()):
                # take as much as we need/have
                rs[r] = min(plant.rate - sum(rs.values()), plant.store[r])
            prs.append((plant, rs))
        print self.name, prs
        return prs

