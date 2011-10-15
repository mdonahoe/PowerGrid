class Auction(object):
    def __init__(self, players, pp_market):
        self.players = players[:]
        self.pp_market = pp_market
        while self.players and pp_market.visible:
            self.auction()

    def auction(self):
        #purchase a single powerplant
        bidders = self.players[:]
        p = bidders.pop(0)
        bid = p.initial_bid(self.pp_market, bidders)
        if not bid:
            self.players.remove(p)
            return
        price, plant = bid
        bidders.append(p)
        while len(bidders) > 1:
            p = bidders.pop(0)
            bid = p.get_bid(price, plant, bidders)
            if bid:
                assert(bid > price)
                price = bid
                bidders.append(p)
        assert(len(bidders) == 1)
        p = bidders[0]
        self.players.remove(p)
        p.buy_power_plant(plant, price)
        self.pp_market.buy(plant)
