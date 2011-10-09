import unittest

import grid
import constants
import step_vars
import player

class TestCity(unittest.TestCase):
    def setUp(self):
        self.sv = step_vars.StepVars(nplayers=2)
        self.city = grid.City('test', self.sv)

    def test_price(self):
        self.assertEqual(10, self.city.price())
        self.sv.step = 2
        self.assertEqual(10, self.city.price())
        self.sv.step = 3
        self.assertEqual(10, self.city.price())
        self.city.buy(player=0)
        self.assertEqual(15, self.city.price())
        self.city.buy(player=1)
        self.assertEqual(20, self.city.price())

    def test_buy(self):
        self.city.buy(player=0)
        self.assertRaises(AssertionError, self.city.buy, 0)
        self.assertEqual([0], self.city.spots)

    def test_can_buy(self):
        self.assertEqual(True, self.city.can_buy(player=0))
        self.city.buy(player=0)
        self.assertEqual(False, self.city.can_buy(player=0))
        self.assertEqual(False, self.city.can_buy(player=1))
        self.sv.step = 2
        self.assertEqual(False, self.city.can_buy(player=0))
        self.assertEqual(True, self.city.can_buy(player=1))


class TestGrid(unittest.TestCase):
    def setUp(self):
        self.sv = step_vars.StepVars(nplayers=2)
        self.grid = grid.Grid(['purple', 'blue', 'yellow'], self.sv)
        self.owned_cities = [self.grid.cities[x] for x in ('erfurt', 'fulda')]
        self.player = player.Player('test')

    def test_costs(self):
        costs = self.grid._costs(self.owned_cities)
        self.assertEqual(8, costs['frankfurt-m'])
        self.assertEqual(26, costs['trier'])
        self.assertEqual(19, costs['dresden'])
        self.assertEqual(39, costs['freiburg'])

    def test_price_for_city(self):
        self.assertEqual(18, self.grid.price_for_city('frankfurt-m', self.owned_cities))
        self.sv.step = 2
        self.grid.cities['frankfurt-m'].buy(player=0)
        self.assertEqual(23, self.grid.price_for_city('frankfurt-m', self.owned_cities))

    def test_price_sorted(self):
        self.player.cities = self.owned_cities
        for city in self.owned_cities:
            city.buy(self.player)
        prices = self.grid.price_sorted(self.player)
        print prices
        self.assertTrue((16, 'leipzig') in prices[:2])
        self.assertTrue((16, 'halle') in prices[:2])

