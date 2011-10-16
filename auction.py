import market

class Auction(object):
    def __init__(self, players, pp_market):
        self.players = players[:]
        self.pp_market = pp_market
        step3started = False
        while self.players:
            try:
                self.auction()
            except market.Step3Error:
                self.pp_market.shuffle(step3=True)
                step3started = True
        if step3started:
            self.pp_market.do_step_three()

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
        # Must buy last b/c this can raise Step3 Error
        self.pp_market.buy(plant)
