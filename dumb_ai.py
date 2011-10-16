import player


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
        print "%s bought %s %s" % (self.name, n, resource)
        print "He has $%s left." % self.money
        print "There are %s %s in the market" % (m.supply, resource)
        plant.stock([resource]*n)

    def build_cities(self, grid):
        if self.cities:
            return
        super(BareMinimumAI, self).build_cities(grid)

    def power_plants_to_use(self):
        return [(p, p.rate * [p.store.keys()[0]]) for p in self.power_plants]
