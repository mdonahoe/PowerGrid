import player
import dumb_ai

class MattAI(player.Player):
    #SUBCLASS STUFF
    def choose_power_plant_to_discard(self):
        """Get rid of the plant with the highest $/city
        calculate an expected value based on the current market"""
        assert(False)

    def redistribute_resources(self,rs):
        """move resources to other power plants and return overflow"""
        assert(False)

    def initial_bid(self, pp_market, bidders):
        """bid on the plant with the lowest $/city"""
        assert(False)

    def get_bid(self,price,plant,bidders):
        assert(False)

    def buy_resources(self, resource_market):
        """Buy enough to power all your plants"""
        assert(False)

    def build_cities(self, grid):
        """Buy as many cities as you can power"""
        assert(False)

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


