


class Map(dict):

    def map(self, func):

        new_map = []
        for k, v in self.iteritems():
            new_map.append(func(k, v))

        return Map(new_map)
