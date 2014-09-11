from unittest import TestCase
from scalafn import List


class TestList(TestCase):

    def test_1(self):
        self.assertEqual([1, 2, 3], [1, 2, 3])
        self.assertEqual(List(1, 2, 3), List(1, 2, 3))
        self.assertEqual(List(1, 2, 3).toList(), List(1, 2, 3))
        self.assertEqual(List(1, 2, 3).toList(), [1, 2, 3])
        self.assertEqual(List(), [])
        self.assertEqual(True, isinstance(List(), list))
        self.assertEqual([True], List(True).toStream())

    def test_repr(self):

        self.assertEqual("List(1, 2, 3)", repr(List(1, 2, 3)))
        self.assertEqual(repr(List(1, 2, 3)), repr(List(1, 2, 3).toStream()))

        # self.assertEqual("""List('1', '2', '3')""", repr(List("1", "2", "3")))
        # self.assertEqual("""ListGenerator(i for i in ['1', '2', '3'])""", repr(List('1', "2", '3').map(_*1)))

    def test_str(self):

        self.assertEqual("List(1, 2, 3)", str(List(1, 2, 3)))

    def test_map(self):
        self.assertEqual(List(1, 2, 3).map(lambda x: x*2), [2, 4, 6])
        self.assertEqual(List().map(lambda x: x*2), [])
        self.assertEqual(List(1, 2, 3).map(lambda x: x*2).toList(), [2, 4, 6])
        self.assertEqual(List().map(lambda x: x*2).toList(), [])

        # self.assertEqual([1, 2, "3", C()],
        #                  List(C(1), C(2), C('3'), C(C())).map(_.a))
        # self.assertEqual([1, 2, "3", C()],
        #                  List(C(1), C(2), C('3'), C(C())).toStream().map(_.a))
        # self.assertEqual([False, True, True],
        #                  List(C(1), C(2), C(3)).map(_.a > 1))
        # self.assertEqual([False, True, True],
        #                  List(C(1), C(2), C(3)).toStream().map(_.a > 1))

    def test_flatten(self):

        self.assertEqual(List(1, 2, 3, 4), [1, 2, 3, 4])
        self.assertEqual(List(List(1, 2), List(3, 4)).flatten().toList(), [1, 2, 3, 4])
        self.assertEqual(List(1, None, 2).flatten().toList(), [1, None, 2])
        self.assertEqual(List(1, None, 2).toStream().flatten(), [1, None, 2])

    def test_mkString(self):

        # self.assertEqual(List().mkString(","), "")
        self.assertEqual("1,2,3", List(1, 2, 3).mkString(","))
        # self.assertEqual(List(1,2,3).map(_ * 2).mkString(","), "1,2,3")
        self.assertEqual(List(1, 2, 3).map(lambda x: x*2).mkString(","), "2,4,6")

    def test_add(self):

        self.assertEqual(List(1, 2, 3), List(1, 2) + 3)
        self.assertEqual(List(1, 2, List(3)), List(1, 2) + List(3))

        self.assertEqual([1, 2, 3, 3, 2, 1], List(1, 2, 3) ++ List(3, 2, 1))
        self.assertEqual([1, 2, 3, 3, 2, 1], List(1, 2, 3) ++ List(3, 2, 1).toStream())

        a = List(1)
        a += 2
        self.assertEqual(List(1, 2), a)

        with self.assertRaises(TypeError):
            self.assertEqual([1, 2, 3, 3, 2, 1], List(1, 2, 3) ++(3, 2, 1))
        with self.assertRaises(TypeError):
            self.assertEqual([1, 2, 3, 3, 2, 1], List(1, 2, 3) ++[3, 2, 1])

        self.assertEqual([1, 2, 3], List(1, 2)+3)

    def test_filter(self):
        self.assertEqual([1], List(1, 2, 3).filter(lambda x: x < 2))
        self.assertEqual([1], List(1, 2, 3).toStream().filter(lambda x: x < 2))

    def test_filterNot(self):

        self.assertEqual([0, '', False], List(*[0, 1, 2, '', True, False]).filterNot(lambda x: x))
        # self.assertEqual([0, '', False], List(*[0, 1, 2, '', True, False]).filterNot(_))

        self.assertEqual([0, '', False], List(*[0, 1, 2, '', True, False]).toStream().filterNot(lambda x: x))
        # self.assertEqual([0, '', False], List(*[0, 1, 2, '', True, False]).toStream().filterNot(_))

        self.assertEqual([2, 3], List(1, 2, 3).filterNot(lambda x: x < 2))
        self.assertEqual([2, 3], List(1, 2, 3).toStream().filterNot(lambda x: x < 2))

        # self.assertEqual([Inner()], List(Inner(), Inner(2), Inner(3)).filterNot(_.a).toList())
        # self.assertEqual([Inner()], List(Inner(), Inner(2), Inner(3)).toStream().filterNot(_.a))

        # self.assertEqual([Inner(2), Inner(3)], List(Inner(1), Inner(2), Inner(3)).filterNot(_.a < 2))
        # self.assertEqual([Inner(2), Inner(3)], List(Inner(1), Inner(2), Inner(3)).toStream().filterNot(_.a < 2))

    '''
    def test_no_side_effect(self):

        init = [1, 2, 3]
        List(*init).map(_*2).filter(_ > 0).flatten().toList()
        self.assertEqual([1, 2, 3], init)
    '''
    def test_iterable(self):

        iter(List(1, 2, 3))
        iter(List(1, 2, 3).toStream())

    def test_groupby(self):
        birds = List("Golden Eagle", "Gyrfalcon", "American Robin", "Mountain BlueBird", "Mountain-Hawk Eagle")
        groupedByFirstLetter = birds.groupBy(lambda x: x[0])

        ret = {"M": List('Mountain BlueBird', 'Mountain-Hawk Eagle'),
               'G': List('Golden Eagle', 'Gyrfalcon'),
               'A': List('American Robin')}

        self.assertEqual(ret, groupedByFirstLetter)

        self.assertEqual({}, List().groupBy(lambda x: x))

        #  groupby with iteratable elements
        lst = [("A", "B"), ("A", "C")]
        self.assertEqual({
            'A': List(*lst)
        }, List(*lst).groupBy(lambda x: x[0]))