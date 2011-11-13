import pprint
import random
import sys

import auction
import constants
import doug_ai
import dumb_ai
import grid
import market
import matt_ai
import player
import powerplant
import stateviz
import step_vars


class Game(object):
    """
    PowerGrid game object has a list of players,
    and manages the rest of the game state.

    Each round is played by calling .round()
    """
    def __init__(self, players, colors=('yellow', 'purple', 'blue')):
        """Create the game"""
        self.players = players
        for p in players:
            p.game = self
        self.step_vars = step_vars.StepVars(len(players))

        self.resource_market = {}
        for args in constants.resource_sub_markets:
            name = args[0]
            m = market.ResourceSubMarket(self.step_vars, *args)
            self.resource_market[name] = m

        self.power_plant_market = market.PowerPlantMarket(self.step_vars, self.players)

        self.grid = grid.Grid(colors, self.step_vars)
        self.stateviz = stateviz.StateViz([p.name for p in self.players], self.resource_market.keys())

    def add_stateviz(self):
        self.stateviz.add_state(dict((p.name, p.get_state()) for p in self.players),
                                dict((name, r.supply) for name, r in self.resource_market.iteritems()))
    def round(self):
        """Process a single round in the game and return a win, if any"""
        self.add_stateviz()
        self.determine_player_order()

        turn_auction = auction.Auction(self.players, self.power_plant_market)
        if not turn_auction.auction_all():
            self.power_plant_market.discard_lowest()
        self.detect_step_three()
        self.buy_resources()
        self.building()
        self.power_plant_market.discard_low_power_plants(self.players)
        self.detect_step_two()
        self.detect_step_three()
        winner = self.detect_game_end()
        if winner:
            self.add_stateviz()
            return winner
        self.bureaucracy()
        self.detect_step_three()

    def print_state(self):
        """print the state of the game"""
        """
        1. players
            a. money
            b. powerplants
            c. resources
        2. cities
        3. power plant market
        4. resource market
        """
        print 'Name\t'+'\t'.join(p.name for p in self.players)
        print 'Money\t'+'\t'.join(str(p.money) for p in self.players)
        print 'Cities\t'+'\t'.join(str(len(p.cities)) for p in self.players)
        for key,m in self.resource_market.iteritems():
            print key,m.supply
        print '-'*40

    def determine_player_order(self):
        """Player order is determined at the end of each round
        The player with the most cities, and highest power plant
        goes first"""
        def compare_players(a, b):
            return (cmp(len(a.cities), len(b.cities))
                    or cmp(a.get_highest_power_plant(),
                           b.get_highest_power_plant()))
        self.players.sort(compare_players, reverse=True)

    def buy_resources(self):
        """Each player buys resources in order"""
        for p in reversed(self.players):
            rs = p.choose_resources_to_buy(self.resource_market)
            if rs:
                p.buy_resources(self.resource_market, rs)  # returns False if they couldn't do it

    def return_resources(self, rs):
        """When a player powers a plant, or discards a plant,
        he may have resources to return to the market"""

        for r,n in rs.iteritems():
            if n == 0: continue
            self.resource_market[r].restock(n)

    def building(self):
        """Each player buys as many plants as they want"""
        for p in reversed(self.players):
            p.build_cities(self.grid)

    def detect_step_two(self):
        """Step 2 happens when a player has a certain number
        of cities. It is possible for step 3 to overtake it"""
        if self.step_vars.step > 1:
            return
        for p in self.players:
            if len(p.cities) >= self.step_vars.cities_for_step2:
                break
        else:
            return
        print 'STEP TWO'

        # One or more players has the required number of cities
        self.step_vars.step = 2
        # Remove ONCE the lowerest numberd power plant from the game
        self.power_plant_market.visible.pop(0)
        # and replace it with a new one from the draw stack,
        # rearranging the market as always.
        self.power_plant_market.draw()

    def detect_step_three(self):
        """Step 3 occurs when the Step 3 card is drawn"""
        if self.step_vars.step == 3:
            return 
        ppm = self.power_plant_market
        if ppm.step3 in ppm.visible:
            ppm.do_step_three()

    def detect_game_end(self):
        """The game ends when 1 player has a certain number of 
        cities"""
        for p in self.players:
            if len(p.cities) >= self.step_vars.cities_for_end:
                break
        else:
            return
        # Now determine the winner
        # Who ever powers the most cities
        # Tie break on Elektro
        rank = [(p.powerable_cities(), p.money, len(p.cities), p) for p in self.players]
        rank.sort()
        return rank[-1][3]

    def bureaucracy(self):
        """In bureaucracy, each player:
        powers their cities
        returns resources
        earns money
        """
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


def play_game(players=None):
    """Play until the game ends with a list of players"""
    if players is None:
        players = [player.HumanPlayer(name) for name in ('doug', 'matt')]
    win = None
    colors = ['yellow', 'purple', 'blue']
    g = Game(players, colors)
    while not win:
        win = g.round()
    print win
    #g.stateviz.plot_states()
    return win

def compete(players, nrounds):
    wins = dict((player.name, 0) for player in players)
    for _ in range(nrounds):
        for player in players: player.clear()
        winner = play_game(players)
        wins[winner.name] += 1
    return wins

if __name__ == '__main__':
    random.seed(0)
    players = [matt_ai.get_ai(sys.argv[1]), doug_ai.get_ai(sys.argv[2])]
    pprint.pprint(compete(players, 100), width=100)
