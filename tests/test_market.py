import unittest

import constants
import market
import step_vars

class TestResourceSubMarket(unittest.TestCase):
    def setUp(self):
        sv = step_vars.StepVars(2)
        args = constants.resource_sub_markets[1]
        self.oil = market.ResourceSubMarket(*args, step_vars=sv)

    def test_market_prices(self):
        """Supply/Demand price tests"""
        sv = step_vars.StepVars(2)
        args = constants.resource_sub_markets[1]
        self.oil = market.ResourceSubMarket(*args, step_vars=sv)

        # make sure quantities are priced correctly
        self.assertEqual(3, self.oil.price_for_n(1))
        self.assertEqual(9, self.oil.price_for_n(3))
        self.assertEqual(13, self.oil.price_for_n(4))

        # cant be more than the supply
        self.assertRaises(market.SupplyError, self.oil.price_for_n, 19)

        # ensure prices change once we buy some stuff
        self.oil.buy(9)
        self.assertEqual(9, self.oil.supply)
        self.assertEqual(6, self.oil.price_for_n(1))

    def test_resupply_restock(self):
        """Test resupplying behavior"""
        # check correct resupply rate
        # with 2 players in step 1, self.oil resupplies 2 at a time
        self.oil.resupply()
        self.oil.resupply()
        self.oil.resupply()
        s = 24
        self.assertEqual(s, self.oil.supply)

        # the supply is now full, and stock is empty
        # resupply should do nothing
        self.oil.resupply()
        self.assertEqual(s, self.oil.supply)

        # a player buys some oil
        self.oil.buy(2)
        # ... but the stock is still empty
        # so resupply does nothing
        self.oil.resupply()
        self.assertEqual(s - 2, self.oil.supply)

        # oil gets restocked
        self.oil.restock(2)
        # resupply works again
        self.oil.resupply()
        self.assertEqual(s, self.oil.supply)

        # additional restocking should fail
        # since the capacity is maxed.
        self.assertRaises(AssertionError, self.oil.restock, 2)
