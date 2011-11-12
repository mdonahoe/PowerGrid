import choose
import constants
import market


class Player(object):
    MAX_POWER_PLANTS = 4

    def __init__(self, name):
        self.name = name
        self.clear()

    def __str__(self):
        return '%s $%s %s %s' % (self.name, self.money, str(self.cities), str(self.power_plants))

    def clear(self):
        self.money = 50
        self.power_plants = []
        self.cities = []
        self.game = None  # set by game

    def buy_power_plant(self,plant,price):
        self.money -= price
        assert self.money >= 0
        self.power_plants.append(plant)
        if len(self.power_plants) > self.MAX_POWER_PLANTS:
            self.discard_power_plant()
        self.power_plants.sort()
        assert len(self.power_plants) <= self.MAX_POWER_PLANTS
        assert plant in self.power_plants, "You can't discard the plant you just bought"

    def discard_power_plant(self):
        plant = self.choose_power_plant_to_discard()
        self.power_plants.remove(plant)
        rs = self.redistribute_resources(plant.store)
        self.game.return_resources(rs)

    def get_highest_power_plant(self):
        if not self.power_plants: return 0
        return max(p.price for p in self.power_plants)

    def total_capacity(self):
        return sum(plant.capacity for plant in self.power_plants)

    def power_cities(self):
        # we have to ask for resources because of hybrids
        plants_resources = self.power_plants_to_use()
        city_count = 0
        for p,rs in plants_resources:
            p.consume(rs)
            self.game.return_resources(rs)
            city_count += p.capacity
        city_count = min(city_count, len(self.cities))
        self.money += constants.payments[city_count]
        return city_count

    def powerable_cities(self):
        capacity = sum([p.capacity for p in self.power_plants if p.can_power()])
        return min(len(self.cities), capacity)

    def get_power_plant_by_price(self,price,power_plants):
        for p in power_plants:
            if p.price==price: return p
        return None

    def can_buy_resource(self, r):
        for p in self.power_plants:
            if p.can_add_resource(r): return True
        return False

    def buy_resources(self, resource_market, rs):
        """You best be buying the right amount."""
        price = 0
        for r, count in rs.iteritems():
            try:
                price += resource_market[r].price_for_n(count)
                if price > self.money:
                    return False
            except market.SupplyError:
                return False
        for r, count in rs.iteritems():
            resource_market[r].buy(count)
        self.money -= price
        return True

    def buy_obvious_resources(self):
        # fill your power plants
        plants = [p for p in self.power_plants if not p.can_power()]

        scenarios = [dict()]
        for p in plants:
            needs = p.resources_needed()
            options = choose.choose(p.store.keys(), needs, r=True)
            new_scenarios = []
            for o in options:
                for s in scenarios:
                    new_s = dict(s)
                    for r in o:
                        new_s[r] = new_s.get(r,0) + 1
                    new_scenarios.append(new_s)
            scenarios = new_scenarios

        # now we have dicts or different groupings of resources we could buy to power our plants.
        # find out how much they cost and return the cheapest one.
        costs = []
        rm = self.game.resource_market
        for rs_to_buy in scenarios:
            try:
                cost = sum([rm[r].cost_for_n(amt) for r, amt in rs_to_by.iteritems()])
            except market.SupplyError:
                # ran out of resources
                continue
            costs.append((cost, rs_to_buy))
        costs.sort()

        cost, rs_to_buy = costs[0]
        # now actually buy it
        for r, amt in rs_to_buy: rm[r].buy(amt)

        # now we need to allocate resources
        # we could just keep track of how this scenario was formed
        # but instead, lets sort

        obvious = [p for p in plants if not p.hybrid]
        hybrid = [p for p in plants if p.hybrid]

        for p in obvious:
            # remove the required resources
            needs = p.resources_needed()
            r = p.store.keys()[0]
            # TODO(matt): stock changed its inputs
            p.stock([r]*needs)
            rs_to_buy[r] = rs_to_buy[r] - needs

        # now do the non-obvious
        # This assumes only coal/oil
        for p in hybrid:
            needs = p.resources_needed()
            a,b = self.store.keys()
            while needs and rs_to_buy.get(a,0):
                rs_to_buy[a]-=1
                needs-=1
            while needs and rs_to_buy.get(b,0):
                rs_to_buy[b]-=1
                needs-=1

        assert sum(rs_to_buy.values())==0, 'Warning: leftover resources'

    #SUBCLASS STUFF
    def choose_power_plant_to_discard(self):
        assert(False)

    def redistribute_resources(self,rs):
        """move resources to other power plants and return overflow"""
        assert(False)

    def initial_bid(self, pp_market, bidders):
        assert(False)

    def get_bid(self,price,plant,bidders):
        assert(False)

    def choose_resources_to_buy(self, resource_market):
        assert(False)

    def build_cities(self, grid):
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

    def redistribute_resources(self,rs):
        discards = {}
        for r in rs:
            print 'Choose a power plant for this %s' % r
            for p in self.power_plants:
                if r not in p.store: continue
                print p
            print '0 to discard'
            choice = self.get_power_plant(True)
            if choice:
                choice.stock({r: 1})
            else:
                discards[r] = discards.get(r, 0) + 1
        return discards

    def initial_bid(self, pp_market, bidders):
        print 'Actual'
        for p in pp_market.actual():
            print '\t%s' % p
        print 'Future'
        for p in pp_market.future():
            print '\t%s' % p
        print 'Other bidders'
        for p in bidders: print '\t%s' % p
        print 'Choose a power plant'
        print '0 to pass'
        p = self.get_power_plant(True, pp_market.actual())
        if not p: return None
        if p.price > self.money:
            print "too 'spensive... lose"
            return None
        print 'Bid %s' % self.name
        while 1:
            price = int(raw_input('$'))
            if price >= p.price: break
            print 'too low'
        return price, p

    def get_bid(self, price, plant, bidders):
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

    def choose_resources_to_buy(self, resource_market):
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

    def build_cities(self, grid):
        print 'Build cities %s' % self.name
        while 1:
            available = []
            for price,city in grid.price_sorted(self):
                available.append(city)
                print '\t$%s %s' %(price,city)
            name = raw_input('city name or (q)uit:')
            if name == 'q': return
            if name not in available:
                print 'no match'
                continue
            city = grid.cities[name]
            price = grid.price_for_city(name,self.cities)
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
                    rs = {p.store.keys()[0]: p.rate}
                else:
                    rs = {}
                    for r in p.store:
                        print 'Amount of %s to use' % r
                        n = int(raw_input(':'))
                        rs[r] = min(n, p.store[r])
                if sum(rs.values()) < p.rate:
                    print 'not enough. dumbass'
                else:
                    prs.append((p,rs))
        return prs

