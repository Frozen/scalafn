from unittest import TestCase
from scalafn import Map


class TestListFunctional(TestCase):

    def test_map(self):

        m = Map({1: 2, 3: 4})

        self.assertEqual({
            2: 4,
            6: 8
        }, m.map(lambda x, y: (x*2, y*2)))

        self.assertEqual({}, Map().map(lambda x, y: (x, y)))

        m = Map({'A': [3, 1, 2], 'B': [5, 0, 4, 1]})

        self.assertEqual({
            'A': [1, 2, 3],
            'B': [0, 1, 4, 5]
        }, m.map(lambda x, y: (x, sorted(y))))

    def test_sub(self):

        self.assertEqual(Map({1: 2}), Map({1: 2, 3: 4}) - 3)
        self.assertEqual(Map({1: 2}), Map({1: 2}) - 3)

