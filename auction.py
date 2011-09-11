class Auction(object):
    def __init__(self,players,market):
        self.players = players[:]
        self.market = market
        while self.players:
            self.auction()

    def auction(self):
        #purchase a single powerplant
        bidders = self.players[:]
        p = bidders.pop(0)
        bid = p.initial_bid(bidders)
        if not bid:
            self.players.remove(p)
            return
        price,plant = bid
        bidders.append(p)
        while len(bidders)>1:
            p = bidders.pop(0)
            bid = p.get_bid(price,plant,bidders)
            print bid,price
            if bid:
                assert(bid > price)
                price = bid
                bidders.append(p)
        assert(len(bidders) == 1)
        print price
        p = bidders[0]
        self.players.remove(p)
        p.buy_power_plant(plant,price)
        self.market.buy(plant)









