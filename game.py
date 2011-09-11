import auction
import constants
import grid
import market
import player
import powerplant
import step_vars

class Game(object):
    def __init__(self,players,colors):
        self.players = players
        for p in players:
            p.game = self
        self.step_vars = step_vars.StepVars(len(players))

        self.resource_market = {}
        for args in constants.resource_sub_markets:
            name = args[0]
            m = market.ResourceSubMarket(*args,step_vars = self.step_vars)
            self.resource_market[name] = m

        self.power_plant_market = market.PowerPlantMarket()

        self.grid = grid.Grid(colors)
    def round(self):
        self.determine_player_order()

        auction.Auction(self.players,self.power_plant_market)

        self.buy_resources()
        self.building()
        self.detect_step_two()
        self.bureaucracy()
    def determine_player_order(self):
        def compare_players(a,b):
            return (cmp(len(a.cities),len(b.cities))
                    or cmp(a.get_highest_power_plant(),
                           b.get_highest_power_plant()))
        self.players.sort(compare_players)
    def buy_resources(self):
        for p in reversed(self.players):
            p.buy_resources()
    def return_resources(self,rs):
        for r in rs:
            self.resource_market[r].restock(1)
    def building(self):
        for p in reversed(self.players):
            p.build_cities()
    def detect_step_two(self): pass
    def bureaucracy(self):
        for p in self.players:
            p.power_cities()
        self.power_plant_market.cycle_deck()
        for _,rm in self.resource_market.iteritems():
            rm.resupply()


if __name__=='__main__':
    players = [player.HumanPlayer(name) for name in ['doug','matt']]
    colors = ['yellow','purple','blue']
    g = Game(players,colors)
    while 1:
        g.round()

