import random
import unittest

import dumb_ai
import game
import powergrid_states

class TestGame(unittest.TestCase):
    """Test the entire game"""
    def test_run_through(self):
        random.seed(1)
        p1 = dumb_ai.PowerAI('Matt')
        p2 = dumb_ai.PowerAI('Doug')
        g = game.Game([p1, p2], ['blue','yellow','purple'])
        print g.power_plant_market.deck
        print g.grid.cities
        p1cities = set()
        p2cities = set()
        def assert_state(game,state):
            print state
            rs = dict((k, m.supply) for k, m in game.resource_market.iteritems())
            state_rs = dict((k,state[k]) for k in game.resource_market)
            p1cities.update(state['p1_new_cities'])
            p2cities.update(state['p2_new_cities'])
            print p1cities, p2cities
            print p1, p2
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
        
        
