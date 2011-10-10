import auction
import constants
import grid
import market
import player
import powerplant
import step_vars


class Game(object):
    def __init__(self, players, colors):
        self.players = players
        for p in players:
            p.game = self
        self.step_vars = step_vars.StepVars(len(players))

        self.resource_market = {}
        for args in constants.resource_sub_markets:
            name = args[0]
            m = market.ResourceSubMarket(self.step_vars, *args)
            self.resource_market[name] = m

        self.power_plant_market = market.PowerPlantMarket(self.step_vars)

        self.grid = grid.Grid(colors, self.step_vars)

    def round(self):
        self.determine_player_order()

        auction.Auction(self.players, self.power_plant_market)

        self.buy_resources()
        self.building()
        self.detect_step_two()
        self.detect_game_end()
        self.bureaucracy()

    def determine_player_order(self):
        def compare_players(a, b):
            return (cmp(len(a.cities), len(b.cities))
                    or cmp(a.get_highest_power_plant(),
                           b.get_highest_power_plant()))
        self.players.sort(compare_players, reverse=True)

    def buy_resources(self):
        for p in reversed(self.players):
            p.buy_resources()

    def return_resources(self, rs):
        for r in rs:
            self.resource_market[r].restock(1)

    def building(self):
        for p in reversed(self.players):
            p.build_cities()

    def detect_step_two(self):
        if self.step_vars.step > 1:
            return
        for p in self.players:
            if len(p.cities) >= self.step_vars.cities_for_step2:
                break
        else:
            return

        # One or more players has the required number of cities
        self.step_vars.step = 2
        # Remove ONCE the lowerest numberd power plant from the game
        # and replace it with a new one from the draw stack,
        # rearranging the market as always.
        self.power_plant_market.draw()

    def detect_game_end(self):
        for p in self.players:
            if len(p.cities) >= self.step_vars.cities_for_end:
                break
        else:
            return
        # Now determine the winner
        # Who ever powers the most
        # Tie break on Elektro

    def bureaucracy(self):
        for p in self.players:
            p.power_cities()
        self.power_plant_market.cycle_deck()
        for _, rm in self.resource_market.iteritems():
            rm.resupply()


if __name__ == '__main__':
    players = [player.HumanPlayer(name) for name in ('doug', 'matt')]
    colors = ['yellow', 'purple', 'blue']
    print players
    g = Game(players, colors)
    while 1:
        g.round()
