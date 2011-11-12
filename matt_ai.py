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
        return rs

    def _initial_bid(self, pp_market, bidders):
        """bid on the plant with the lowest $/city"""
        return None

    def _get_bid(self,price,plant,bidders):
        return 0

    def _buy_resources(self, resource_market):
        """Buy enough to power all your plants"""
        pass

    def _build_cities(self, grid):
        """Buy as many cities as you can power"""
        pass

    def _power_plants_to_use(self):
        """
        Power all ecos
        power from most expensive down
        until we can power all cities
        """
        return []

