from future.builtins import *  # required!!


class Map(dict):

    if not hasattr(dict, 'iteritems'):
        iteritems = dict.items

    def map(self, func):

        new_map = []
        for k, v in self.iteritems():
            new_map.append(func(k, v))

        return Map(new_map)

    def __sub__(self, other):
        """
        Substraction

        assert Map({1: 2, 3: 4}) - 3 == Map({1: 2})

        :param other:
        :return:
        """
        self.pop(other, None)
        return self
