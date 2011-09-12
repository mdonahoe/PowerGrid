#network stuff
import constants

class City(object):
    def __init__(self,name):
        self.name = name
        self.spots = []
    def price(self):
        return 10
        #0:10
        #1:15
        #2:20
    def buy(self,player):
        assert(self.can_buy())
        self.spots.append(player)
    def can_buy(self):
        return len(self.spots)==0
    def __str__(self):
        return self.name
    def __repr__(self):
        return "City('%s')" % self.name

class Grid(object):
    def __init__(self,colors):
        #get a list of cities for this game
        cities = []
        for c in colors:
            cities.extend(constants.colors[c])

        #create maps
        self.cities = {}
        self.graph = {}
        for c in cities:
            self.cities[c] = City(c)
            self.graph[c] = {}

        #attach edges
        for node in self.cities:
            if node not in constants.network: continue
            for neighbor,cost in constants.network[node].iteritems():
                if neighbor not in self.cities: continue
                self.graph[node][neighbor] = cost
                self.graph[neighbor][node] = cost

    def __str__(self):
        return '\n\t'.join(['Cities']+self.cities.keys())
    def _costs(self,owned_cities):
        #assume I can have many roots
        if not owned_cities:
            costs = dict((c,0) for c in self.cities)
            return costs
        costs = dict((c.name,0) for c in owned_cities)
        queue = [c.name for c in owned_cities[:]]
        while queue:
            node = queue.pop(0)
            for neighbor,cost in self.graph[node].iteritems():
                c = cost + costs[node]
                if neighbor not in costs or c < costs[neighbor]:
                    costs[neighbor] = c
                    queue.append(neighbor)
        return costs
    def price_for_city(self,cityname,owned_cities):
        city = self.cities[cityname]
        cs = self._costs(owned_cities)
        return cs[cityname] + city.price()
    def price_sorted(self,owned_cities):
        costs = self._costs(owned_cities)
        prices = []
        for name,cost in costs.iteritems():
            city = self.cities[name]
            if not city.can_buy(): continue
            prices.append((cost + city.price(), name))
        prices.sort()
        return prices
    def bfs(self,root):
        """breadth-first search algorithm"""
        prev = {}
        costs = {root:0}
        queue = [root]
        while queue:
            node = queue.pop(0)
            for neighbor,cost in self.graph[node].iteritems():
                c = cost + costs[node]
                if neighbor not in costs or c < costs[neighbor]:
                    costs[neighbor] = c
                    prev[neigbor] = node
                    queue.append(neighbor)
        return prev,costs




