import constants

class Player(object):
    MAX_POWER_PLANTS = 4
    def __init__(self,name):
        self.name = name
        self.money = 50
        self.power_plants = []
        self.cities = []
        self.game = None #set by game
    def __str__(self):
        return '%s $%s' % (self.name, self.money)
    def buy_power_plant(self,plant,price):
        print price
        self.money -= price
        assert(self.money >= 0)
        self.power_plants.append(plant)
        if len(self.power_plants) > self.MAX_POWER_PLANTS:
            self.discard_power_plant()
        assert(len(self.power_plants) <= self.MAX_POWER_PLANTS)
    def discard_power_plant(self):
        plant = self.choose_plant_to_discard(self)
        self.power_plants.remove(plant)
        rs = self.redistribute_resources(plant.store)
        self.game.return_resources(rs)

    def get_highest_power_plant(self):
        if not self.power_plants: return 0
        return max(p.price for p in self.power_plants)
    def power_cities(self):
        plants_resources = self.power_plants_to_use()
        city_count = 0
        for p,rs in plants_resources:
            p.consume(rs)
            self.game.return_resources(rs)
            city_count += p.capacity
        city_count = min(city_count, len(self.cities))
        self.money += constants.payments[city_count]
    def get_power_plant_by_price(self,price,power_plants):
        for p in power_plants:
            if p.price==price: return p
        return None
    def can_buy_resource(self, r):
        for p in self.power_plants:
            if p.can_add_resource(r): return True
        return False
    #SUBCLASS STUFF
    def choose_power_plant_to_discard(self):
        assert(False)
    def redistribute_resources(self,rs):
        """move resources to other power plants and return overflow"""
        assert(False)
    def initial_bid(self,bidders):
        assert(False)
    def get_bid(self,price,plant,bidders):
        assert(False)
    def buy_resources(self):
        assert(False)
    def build_cities(self):
        assert(False)
    def power_plants_to_use(self):
        assert(False)

class HumanPlayer(Player):
    def choose_power_plant_to_discard(self):
        print "Discard a power plant"
        print self.power_plants
        while 1:
            price = int(raw_input(':'))
            for p in self.power_plants:
                if p.price==price: return p
            print 'no matching price'
    def get_power_plant(self,accept_zero=False,power_plants=None):
        if power_plants is None:
            power_plants = self.power_plants
        while 1:
            price = int(raw_input(':'))
            if accept_zero and price==0: return None
            p = self.get_power_plant_by_price(price,power_plants)
            if p: return p
            print 'no match'
    def get_response(self,choices):
        while 1:
            choice=raw_input(':')
            if choice in choices: return choice
            print 'no match'
            """doug ducks"""

    def redistribute_resources(self,rs):
        discards = []
        for r in rs:
            print 'Choose a power plant for this %s' % r
            for p in self.power_plants:
                if r not in p.store: continue
                print p
            print '0 to discard'
            choice = self.get_power_plant(True)
            if choice:
                choice.stock([r])
            else:
                discards.append(r)
        return discards
    def initial_bid(self,bidders):
        print 'Actual'
        for p in self.game.power_plant_market.actual():
            print '\t%s' % p
        print 'Future'
        for p in self.game.power_plant_market.future():
            print '\t%s' % p
        print 'Other bidders'
        for p in bidders: print '\t%s' % p
        print 'Choose a power plant'
        print '0 to pass'
        p = self.get_power_plant(True,self.game.power_plant_market.actual())
        if not p: return None
        if p.price > self.money:
            print "too 'spensive... lose"
            return None
        print 'Bid %s' % self.name
        while 1:
            price = int(raw_input('$'))
            if price >= p.price: break
            print 'too low'
        return price,p


    def get_bid(self,price,plant,bidders):
        if price >= self.money:
            print 'not enough money to bid'
            return 0
        print "Bid %s" % self.name
        print 'current bid = %s' % price
        print '0 to pass'
        while 1:
            bid = int(raw_input('$'))
            if bid > price: break
            if bid == 0: return 0
            print 'too low, dick'
        if bid > self.money:
            print 'not enough money, trimming'
            bid = self.money
        return bid

    def buy_resources(self):
        print 'Resource Market'
        for r,m in self.game.resource_market.iteritems():
            print '\t %s' % m
        rs = []
        for r,m in self.game.resource_market.iteritems():
            if not self.can_buy_resource(r): continue
            print 'Amount of %s to buy' % r
            n = int(raw_input(':'))
            price = m.price_for_n(n)
            if price > self.money:
                print 'NO %s FOR YOU!' % r
                continue
            self.money -= price
            m.buy(n)
            rs.extend([r]*n)
        discards = self.redistribute_resources(rs)
        if discards:
            print 'idiot'
        self.game.return_resources(discards)

    def build_cities(self):
        print 'Build cities %s' % self.name
        while 1:
            available = []
            for price,city in self.game.grid.price_sorted(self.cities):
                available.append(city)
                print '\t$%s %s' %(price,city)
            name = raw_input('city name or (q)uit:')
            if name == 'q': return
            if name not in available:
                print 'no match'
                continue
            city = self.game.grid.cities[name]
            price = self.game.grid.price_for_city(name,self.cities)
            if price > self.money:
                print 'you tried to spent too much. done'
                return
            self.cities.append(city)
            city.buy(self)
            self.money -= price
    def power_plants_to_use(self):
        #todo, let them redistribute
        prs = []
        print self.power_plants
        print "You have %s cities" % len(self.cities)
        for p in self.power_plants:
            if not p.can_power(): continue
            print p
            yn = raw_input('power y/n ?').lower()
            if yn=='y':
                if p.obvious_power():
                    rs = [p.store.keys()[0]]*p.rate
                else:
                    rs = []
                    for r in p.store:
                        print 'Amount of %s to use' % r
                        n = int(raw_input(':'))
                        rs.extend([r]*min(n,p.store[r]))
                if len(rs) < p.rate:
                    print 'not enough. dumbass'
                else:
                    prs.append((p,rs))
        return prs


