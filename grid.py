#network stuff
import constants


class City(object):
    """The City is a space on the board"""
    prices = [10, 15, 20]

    def __init__(self, name, step_vars):
        self.name = name
        self.spots = []
        self.step_vars = step_vars

    def price(self):
        """A city's cost is a function of the number of owners"""
        return self.prices[len(self.spots)]

    def buy(self, player):
        """The player and the city keep track of each other"""
        assert self.can_buy(player)
        self.spots.append(player)

    def can_buy(self, player):
        """Players can't own the same city twice
        And the number of possible owners is a function of the Step"""
        if player in self.spots:
            return False
        return len(self.spots) < self.step_vars.step

    def __str__(self):
        return self.name

    def __repr__(self):
        return "City('%s')" % self.name


class Grid(object):
    """The grid is the network of cities"""
    def __init__(self, colors, step_vars):
        #get a list of cities for this game
        cities = []
        for c in colors:
            cities.extend(constants.colors[c])

        #create maps
        self.cities = {}
        self.graph = {}
        for c in cities:
            self.cities[c] = City(c, step_vars)
            self.graph[c] = {}

        #attach edges
        for node in self.cities:
            if node not in constants.network:
                continue
            for neighbor, cost in constants.network[node].iteritems():
                if neighbor not in self.cities:
                    continue
                self.graph[node][neighbor] = cost
                self.graph[neighbor][node] = cost

    def __str__(self):
        return '\n\t'.join(['Cities'] + self.cities.keys())

    def _costs(self, owned_cities):
        """Do a BFS on the network to find the cheapest price to each city,
        given the player's current cities"""
        # assume I can have many roots
        if not owned_cities:
            costs = dict((c, 0) for c in self.cities)
            return costs
        costs = dict((c.name, 0) for c in owned_cities)
        queue = [c.name for c in owned_cities[:]]
        while queue:
            node = queue.pop(0)
            for neighbor, cost in self.graph[node].iteritems():
                c = cost + costs[node]
                if neighbor not in costs or c < costs[neighbor]:
                    costs[neighbor] = c
                    queue.append(neighbor)
        return costs

    def price_for_city(self, cityname, owned_cities):
        """A player needs to pay for the 'pipeline' and the
        cost of a city in order to build there."""
        city = self.cities[cityname]
        cs = self._costs(owned_cities)
        return cs[cityname] + city.price()

    def price_sorted(self, player):
        """Return a list of cheapest cities"""
        costs = self._costs(player.cities)
        prices = []
        for name, cost in costs.iteritems():
            city = self.cities[name]
            if not city.can_buy(player):
                continue
            prices.append((cost + city.price(), name))
        prices.sort()
        return prices
