import market

class Auction(object):
    def __init__(self, players, pp_market):
        self.players = players[:]
        self.pp_market = pp_market

    def auction_all(self):
        any_bought = False
        while self.players and self.pp_market.visible:
            if self._auction():
                any_bought = True
        return any_bought

    def _auction(self):
        #purchase a single powerplant
        bidders = self.players[:]
        p = bidders.pop(0)
        bid = p.initial_bid(self.pp_market, bidders)
        if not bid:
            self.players.remove(p)
            return False
        price, plant = bid
        bidders.append(p)
        while len(bidders) > 1:
            p = bidders.pop(0)
            bid = p.get_bid(price, plant, bidders)
            if bid:
                assert bid > price
                price = bid
                bidders.append(p)
        assert len(bidders) == 1
        p = bidders[0]
        self.players.remove(p)
        p.buy_power_plant(plant, price)
        self.pp_market.buy(plant)
        return True
