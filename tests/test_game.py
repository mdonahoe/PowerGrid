import pprint
import random
import unittest

import dumb_ai
import game
import powergrid_states

def Step3Shuffle(deck):
    plants = dict((plant.price, plant) for plant in deck)
    [deck.pop() for _ in plants]
    deck.extend([plants[price] for price in [34,13,40,39,32,46,44,37]])

class TestGame(unittest.TestCase):
    """Test the entire game"""
    def test_run_through(self):
        random.seed(1)
        p1 = dumb_ai.PowerAI('Matt')
        p2 = dumb_ai.PowerAI('Doug')
        g = game.Game([p1, p2], ['blue','yellow','purple'])
        random.shuffle = Step3Shuffle
        print g.power_plant_market.deck
        print g.grid.cities
        p1cities = set()
        p2cities = set()
        def assert_state(game,state):
            pprint.pprint(state, indent=2, depth=2, width=2)
            rs = dict((k, m.supply) for k, m in game.resource_market.iteritems())
            state_rs = dict((k,state[k]) for k in game.resource_market)
            p1cities.update(state['p1_new_cities'])
            p2cities.update(state['p2_new_cities'])
            pprint.pprint(p1cities, indent=2, depth=2, width=2)
            pprint.pprint(p2cities, indent=2, depth=2, width=2)
            print p1
            print p2
            self.assertEqual(rs,state_rs)
            self.assertEqual(state['p1_money'], p1.money)
            self.assertEqual(state['p1_plants'], [plant.price for plant in p1.power_plants])
            self.assertEqual(p1cities, set(c.name for c in p1.cities))

            self.assertEqual(state['p2_money'], p2.money)
            self.assertEqual(state['p2_plants'], [plant.price for plant in p2.power_plants])
            self.assertEqual(p2cities, set(c.name for c in p2.cities))
        win = None
        states = powergrid_states.states
        assert_state(g,states.pop(0))
        i=0
        while win is None:
            print i
            i += 1
            win = g.round()
            assert_state(g,states.pop(0))
        
        
