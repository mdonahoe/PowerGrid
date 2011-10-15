import unittest

import player

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = player.Player('testie')

    def test_buy_power_plant(self):
        self.player.buy_power_plant('plant', 16)
        self.assertEquals(34, self.player.money)
        self.assertEquals(['plant'], self.player.power_plants)
        self.player.buy_power_plant('plant 2', 8)
        self.player.buy_power_plant('plant 3', 8)
        self.assertRaises(AssertionError, self.player.buy_power_plant,
                          'plant 4', 50)
        self.player.money = 50
        self.player.buy_power_plant('plant 4', 8)
        self.player.discard_power_plant = lambda: None
        self.assertRaises(AssertionError, self.player.buy_power_plant,
                          'plant 5', 1)
        self.player.power_plants.pop()
        self.player.discard_power_plant = (
                lambda: self.player.power_plants.pop(0))
        self.player.buy_power_plant('plant 5', 1)
        self.assertEquals(['plant 2', 'plant 3', 'plant 4', 'plant 5'],
                          self.player.power_plants)

    
