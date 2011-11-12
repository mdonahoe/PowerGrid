import dumb_ai
import player
import copy


def get_ai(ai):
    if ai == 'DougAI':
        return DougAI('Doug')
    if ai == 'PowerAI':
        return dumb_ai.SuperPowerAI('Doug')

class DougAI(player.SafePlayer):

    def _choose_power_plant_to_discard(self):
        """Always remove the cheapest"""
        return self.power_plants[0]

    def _redistribute_resources(self, rs):
        for plant in reversed(self.power_plants):
            rs = plant.better_stock(rs)

        return rs

    def _initial_bid(self, pp_market, bidders):
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

    def _get_bid(self, price, plant, bidders):
        return 0

    def _choose_resources_to_buy(self, resource_market):
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

    def other_player(self):
        for player in self.game.players:
            if player != self:
                return player

    def _build_cities(self, grid):
        """Buy as many as you can power
        starting with cheapest and alphabetically"""
        print '%s buying cities' % self.name
        other_player = self.other_player()
        if (len(other_player.cities) <= len(self.cities)
            and sum(city[0] for city in cities) > self.money):
            return 

        while True:
            cities = grid.price_sorted(self.cities)
            #print cities[:2], self.name, self.money
            if not cities:
                #print self.cities
                #print set([city.name for city in self.cities])-set(grid.cities.keys())
                return
            price, name = cities[0]
            city = grid.cities[name]
            if price > self.money:
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
