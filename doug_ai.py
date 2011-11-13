import operator

import dumb_ai
import player


def get_ai(ai):
    if ai == 'DougAI':
        return DougAI('Doug')
    if ai == 'PowerAI':
        return dumb_ai.SuperPowerAI('Doug')

class DougAI(player.SafePlayer):

    def _choose_power_plant_to_discard(self):
        """Always remove the cheapest"""
        capacity_sorted = sorted(self.power_plants, key=operator.attrgetter('capacity', 'price'))
        return capacity_sorted[0]

    def _redistribute_resources(self, rs):
        for plant in reversed(self.power_plants):
            rs = plant.better_stock(rs)
        return rs

    def _initial_bid(self, pp_market, bidders):
        """Bid on the highest non-hybrid"""
        print 'actual market: ', [plant.price for plant in pp_market.actual()]
        maxed_out = len(self.cities) < self.total_capacity()
        reverse_capacity_sorted = sorted(pp_market.actual(), key=operator.attrgetter('capacity', 'price'), reverse=True)
        owned_capacity_sorted = sorted(self.power_plants, key=operator.attrgetter('capacity', 'price'))
        for plant in reverse_capacity_sorted:
            if plant.price > self.money:
                continue
            if len(self.power_plants) == 4 and owned_capacity_sorted[0].capacity > plant.capacity:
                return None
            if maxed_out and owned_capacity_sorted[0] - plant.capacity < 1:
                return None
                
            print self.name, 'bids on', plant.price
            return plant.price, plant
        print '%s passed' % self.name
        return None

    def _get_bid(self, price, plant, bidders):
        return 0

    def _choose_resources_to_buy(self, resource_market):
        """Buy resources for all powerplants, decreasing"""
        self.buy_obvious_resources()
        
    def other_player(self):
        for player in self.game.players:
            if player != self:
                return player

    def _build_cities(self, grid):
        """Buy as many as you can power
        starting with cheapest and alphabetically"""
        print '%s buying cities' % self.name
        other_player = self.other_player()
        total_price = 0
        bought_cities = self.cities[:]
        while True:
            cities = grid.price_sorted(bought_cities)
            if not cities: break
            total_price += cities[0][0]
            bought_cities.append(grid.cities[cities[0][1]])
        if ((len(bought_cities) != 21 or total_price > self.money)
            and len(other_player.cities) <= len(self.cities)):
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
