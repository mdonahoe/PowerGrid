import player
import market


class DumbAI(player.Player):
    def choose_power_plant_to_discard(self):
        return self.power_plants[0]

    def redistribute_resources(self,rs):
        """move resources to other power plants and return overflow"""
        return rs

    def initial_bid(self, pp_market, bidders):
        actual = pp_market.actual()
        if not actual:
            return None
        cheapest = pp_market.actual()[0]
        if cheapest.price <= self.money:
            return cheapest.price, cheapest
        return None

    def get_bid(self, price, plant, bidders):
        return None

    def buy_resources(self, resource_market):
        return None

    def build_cities(self, grid):
        cities = grid.price_sorted(self)
        if not cities:
            return
        (price, cheapest) = cities[0]
        cheapest = grid.cities[cheapest]
        if price <= self.money:
            self.money -= price
            cheapest.buy(self)
            self.cities.append(cheapest)

    def power_plants_to_use(self):
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

    def buy_resources(self, resource_market):
        if not self.power_plants:
            return None
        plant = self.power_plants[0]
        resource = plant.store.keys()[0]
        n = plant.resources_needed()
        if resource == 'eco': return
        m = resource_market[resource]
        resource_market[resource].buy(n)
        plant.stock([resource]*n)

    def build_cities(self, grid):
        if self.cities:
            return
        super(BareMinimumAI, self).build_cities(grid)

    def power_plants_to_use(self):
        return [(p, p.rate * [p.store.keys()[0]]) for p in self.power_plants]


class Outbidder(DumbAI):
    """always tries to outbid you"""
    def get_bid(self, price, plant, bidders):
        if price < self.money:
            return price + 1
        return None

class BasicAI(DumbAI):
    """Buys a new power plant, resources, and a city every round"""
    def buy_resources(self, resource_market):
        for plant in self.power_plants:
            resource = plant.store.keys()[0]
            n = plant.resources_needed()
            if n == 0: continue
            m = resource_market[resource]
            m.buy(n)
            plant.stock([resource]*n)
    def power_plants_to_use(self):
        return [(p, p.rate * [p.store.keys()[0]]) for p in self.power_plants]

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
        for plant in reversed(pp_market.actual()):
            if plant.hybrid or plant.price > self.money:
                continue
            print self.name, plant.price, pp_market.visible
            return plant.price, plant
        return None

    def get_bid(self,price,plant,bidders):
        """Bid only when the cheapest future plant
        is the same price as plant.price + 1"""
        if price!=plant.price:
            return 0
        if price >= self.money:
            return 0
        if self.game.step_vars.step == 3:
            return 0    
        future = self.game.power_plant_market.future()[0]
        if price + 1 == future.price:
            print 'outbid', self.name, plant.price
            return price + 1
        return 0

    def buy_resources(self, resource_market):
        """Buy resources for all powerplants, decreasing"""
        for plant in reversed(self.power_plants):
            n = plant.resources_needed()
            if n <= 0:
                continue
            resource = plant.store.keys()[0]
            try:
                price = resource_market[resource].price_for_n(n)
                if price > self.money:
                    continue
                resource_market[resource].buy(n)
                self.money -= price
                plant.stock([resource] * n)
            except market.SupplyError:
                continue

    def build_cities(self, grid):
        """Buy as many as you can power
        starting with cheapest and alphabetically"""
        while True:
            cities = grid.price_sorted(self)
            print cities[:2], self.name
            price, name = grid.price_sorted(self)[0]
            city = grid.cities[name]
            if price > self.money or len(self.cities) >= self.total_capacity():
                break
            self.cities.append(city)
            city.buy(self)
            self.money -= price

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
                prs.append((plant, []))
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
            prs.append((plant, [plant.store.keys()[0]] * plant.rate))
        print self.name, prs 
        return prs

