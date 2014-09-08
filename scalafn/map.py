from future.builtins import *  # required!!


class Map(dict):

    if not hasattr(dict, 'iteritems'):
        iteritems = dict.items

    def map(self, func):

        new_map = []
        for k, v in self.iteritems():
            new_map.append(func(k, v))

        return Map(new_map)
