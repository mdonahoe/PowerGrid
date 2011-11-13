from matplotlib import pyplot


class StateViz(object):

    def __init__(self, players, resources):
        self.players = dict((player, []) for player in players)
        self.resources = dict((resource, []) for resource in resources)

    def add_state(self, player_states, resource_states):
        for player, state in player_states.iteritems():
            self.players[player].append(state)
        for resource, state in resource_states.iteritems():
            self.resources[resource].append(state)

    def plot_series(self, series, name):
        pyplot.figure()
        colors = ['bo', 'ro']
        for series_name, values in series.iteritems():
            color = colors.pop()
            pyplot.plot(values, color, label=series_name)
        pyplot.title(name)
        loc = 'upper right'
        if name not in self.resources:
            loc = 'upper left'
        pyplot.legend(loc=loc)

    def build_series(self, data, series_name):
        series = {}
        for name in data:
            series[name] = [d[series_name] for d in data[name]]
        return series

    def plot_states(self):
        for key in self.players.values()[0][0]:
            self.plot_series(self.build_series(self.players, key), key)
        pyplot.show()


"""
pyplot.axis([min(sell_times) - time_range * .05,
             max(sell_times) + time_range * .05,
             min(prices) - price_range * .05,
             max(prices) + price_range * .05])
"""
