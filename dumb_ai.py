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

    def buy_resources(self):
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

