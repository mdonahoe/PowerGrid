import dumb_ai
import player

def get_ai(ai):
    if ai == 'DougAI':
        return DougAI('Doug')
    if ai == 'PowerAI':
        return dumb_ai.SuperPowerAI('Doug')

class DougAI(player.SafePlayer):
    def _choose_power_plant_to_discard(self):
        return self.power_plants[0]

    def _redistribute_resources(self, rs):
        return rs

    def _initial_bid(self, pp_market, bidders):
        return None

    def _get_bid(self, price, plant, bidders):
        return 0

    def _choose_resources_to_buy(self, resource_market):
        pass

    def _build_cities(self, grid):
        pass

    def _power_plants_to_use(self):
        return []
