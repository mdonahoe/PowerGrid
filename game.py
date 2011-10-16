import auction
import constants
import dumb_ai
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
        winner = self.detect_game_end()
        if winner:
            return winner
        self.bureaucracy()

    def determine_player_order(self):
        def compare_players(a, b):
            return (cmp(len(a.cities), len(b.cities))
                    or cmp(a.get_highest_power_plant(),
                           b.get_highest_power_plant()))
        self.players.sort(compare_players, reverse=True)

    def buy_resources(self):
        for p in reversed(self.players):
            p.buy_resources(self.resource_market)

    def return_resources(self, rs):
        # rs is either a list of strings, or a dict
        if type(rs)==type([]):
            _rs = {}
            for r in rs: _rs[r] = _rs.get(r, 0) + 1
        else:
            _rs = rs

        for r,n in _rs.iteritems():
            if n == 0: continue
            self.resource_market[r].restock(n)

    def building(self):
        for p in reversed(self.players):
            p.build_cities(self.grid)

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
        self.power_plant_market.visible.pop(0)
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
        # Who ever powers the most cities
        # Tie break on Elektro
        rank = [(p.power_cities(), p.money, p) for p in self.players]
        rank.sort()
        return rank[-1][2]

    def bureaucracy(self):
        for p in self.players:
            p.power_cities()
        for _, rm in self.resource_market.iteritems():
            rm.resupply()
        # This has to be after resupply b/c you resupply at step 2 rates if
        # step 3 is triggered here.
        try:
            self.power_plant_market.cycle_deck()
        except market.Step3Error:
            self.power_plant_market.do_step_three()


if __name__ == '__main__':
    if 0:
        players = [player.HumanPlayer(name) for name in ('doug', 'matt')]
    players = [dumb_ai.DumbAI('Bill'), dumb_ai.BareMinimumAI('Ted')]
    colors = ['yellow', 'purple', 'blue']
    print players
    g = Game(players, colors)
    win = None
    while win is None:
        win = g.round()
    print win, win.name
