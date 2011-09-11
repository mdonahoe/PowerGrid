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
        for node in constants.network:
            for neighbor,cost in constants.network[c].iteritems():
                if neighbor not in self.cities: continue
                self.graph[node][neighbor] = cost
                self.graph[neighbor][node] = cost
    def _costs(self,owned_cities):
        #assume I can have many roots
        costs = dict((c,0) for c in owned_cities)
        queue = owned_cities[:]
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
        return self._costs(owned_cities)[cityname] + city.price()
    def cheapest(self,owned_cities):
        costs = self._costs(owned_cities)
        prices = []
        for city,cost in costs.iteritems():
            if city in owned_cities: continue
            prices.append((cost + self.cities[city].price(),city))
        prices.sort()
        return prices[0]
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




