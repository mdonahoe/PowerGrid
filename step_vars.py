"""Step Variables"""

resupply_rates = {
    'coal': {
        2:[3,4,3],
        3:[4,5,3],
        4:[5,6,4],
        5:[5,7,5],
        6:[7,9,6]
    },
    'oil': {
        2:[2,2,4],
        3:[2,3,4],
        4:[3,4,5],
        5:[4,5,6],
        6:[5,6,7]
    },
    'garbage': {
        2:[1,2,3],
        3:[1,2,3],
        4:[2,3,4],
        5:[3,3,5],
        6:[3,5,6],
    },
    'uranium': {
        2:[1,1,1],
        3:[1,1,1],
        4:[1,2,2],
        5:[2,3,2],
        6:[2,3,3]
    }
}


class StepVars(object):
    """Object which holds Step-dependent variables"""
    def __init__(self, nplayers):
        assert nplayers > 1, "Not enough players"
        assert nplayers < 7, "Too many players"
        self.nplayers = nplayers
        self.step = 1
        N = nplayers - 2
        # Number of regions chosen on the map
        self.regions = [3, 3, 4, 5, 5][N]
        # Number of randomly removed face-down power plants 
        # (after preparing the market)
        self.power_plants_to_remove = [8, 8, 4, 0, 0][N]
        # Maximum number of power plants owned by a player
        self.max_plants_per_player = [4, 3, 3, 3, 3][N]
        # Number of connected cities to trigger step 2
        self.cities_for_step2 = [10, 7, 7, 7, 6][N]
        # Number of connected cities to trigger game end
        self.cities_for_end = [21, 17, 17, 15, 14][N]

    def get_resupply_rate(self, resource):
        return resupply_rates[resource][self.nplayers][self.step-1]
