import dumb_ai
import player

def get_ai(ai):
    if ai == 'MattAI':
        return MattAI('Matt')
    if ai == 'PowerAI':
        return dumb_ai.SuperPowerAI('Matt')

class MattAI(player.SafePlayer):
    def _choose_power_plant_to_discard(self):
        """Get rid of the plant with the highest $/city
        calculate an expected value based on the current market"""
        return self.power_plants[0]

    def _redistribute_resources(self,rs):
        """move resources to other power plants and return overflow"""
        for plant in reversed(self.power_plants):
            rs = plant.better_stock(rs)

        return rs

    def _initial_bid(self, pp_market, bidders):
        """bid on the plant with the lowest $/city"""
        if len(self.cities) < self.total_capacity():
            return None
        for plant in reversed(pp_market.actual()):
            if plant.price > self.money:
                continue
            if len(self.power_plants) == 4 and plant.price < min([x.price for x in self.power_plants]):
                return None
            return plant.price, plant
        return None

    def _get_bid(self,price,plant,bidders):
        return 0

    def _buy_resources(self, resource_market):
        """Buy enough to power all your plants"""
        for plant in reversed(self.power_plants):
            n = plant.resources_needed()
            if n <= 0:
                continue
            resource = sorted(plant.store.keys())[0]
            print '\tneed %s %s' % (n, resource)
            if self.buy_resources(resource_market, {resource: n}):
                plant.stock({resource: n})

    def _build_cities(self, grid):
        """Buy as many cities as you can power"""
        while True:
            cities = grid.price_sorted(self)
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

    def _power_plants_to_use(self):
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

