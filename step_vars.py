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
    def __init__(self, nplayers):
        self.nplayers = nplayers
        self.step = 1

    def get_resupply_rate(self, resource):
        return resupply_rates[resource][self.nplayers][self.step-1]
