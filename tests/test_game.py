import pprint
import random
import unittest

import dumb_ai
import game
import states2

def Step3Shuffle(deck):
    plants = dict((plant.price, plant) for plant in deck)
    [deck.pop() for _ in plants]
    deck.extend([plants[price] for price in [34,13,40,39,32,46,44,37]])

class TestGame(unittest.TestCase):
    """Test the entire game"""
    def test_ai_battle(self):
        for i in range(1):
            players = [
                dumb_ai.PowerAI('Steve'),
                dumb_ai.DumbAI('Trip'),
                dumb_ai.Outbidder('Goof'),
            ]
            self.assertEqual(game.play_game(players).name, 'Steve')

    def test_run_through(self):
        random.seed(1)
        p1 = dumb_ai.PowerAI('Matt')
        p2 = dumb_ai.PowerAI('Doug')
        g = game.Game([p1, p2], ['blue','yellow','purple'])
        random.shuffle = Step3Shuffle
        p1cities = set()
        p2cities = set()
        def assert_state(game,state,winner):
            if winner:
                self.assertEqual(winner.name, state['winner'])
            rs = dict((k, m.supply) for k, m in game.resource_market.iteritems())
            print 'Resources:', rs
            state_rs = dict((k,state[k]) for k in game.resource_market)
            p1cities.update(state['p1_new_cities'])
            p2cities.update(state['p2_new_cities'])
            self.assertEqual(rs,state_rs)
            self.assertEqual(state['p1_money'], p1.money)
            self.assertEqual(state['p1_plants'], [plant.price for plant in p1.power_plants])
            self.assertEqual(p1cities, set(c.name for c in p1.cities))

            self.assertEqual(state['p2_money'], p2.money)
            self.assertEqual(state['p2_plants'], [plant.price for plant in p2.power_plants])
            self.assertEqual(p2cities, set(c.name for c in p2.cities))
        win = None
        states = states2.states
        current = states.pop(0)
        i= -1
        while 'run' in current:
            i += 1
            print '-------End of TURN %s----------' % i
            print 'Players'
            for player in g.players:
                print player.name
                print player.power_plants
                print '%s cities %s' % (len(player.cities), player.cities)
                print '$%s' % player.money
                print '~~~~~~~~~~~~'
            print 'Market: %s' %  ', '.join(str(p.price) for p in g.power_plant_market.visible)
            assert_state(g,current,win)
            if win: break
            print '--------START of TURN %s-------' % (i + 1)
            current = states.pop(0)
            win = g.round()
            
