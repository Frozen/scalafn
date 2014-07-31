from unittest import TestCase, skip

from scalafn.run3 import List, _


class TestFunctional(TestCase):

    def test_1(self):
        self.assertEqual([1, 2, 3], [1, 2, 3])
        self.assertEqual(List(1, 2, 3), List(1, 2, 3))
        self.assertEqual(List(1, 2, 3).toList(), List(1, 2, 3))
        self.assertEqual(List(1, 2, 3).toList(), [1, 2, 3])
        self.assertEqual(List(), [])
        self.assertEqual(True, isinstance(List(), list))

    # @skip
    def test_repr(self):

        self.assertEqual("List(1, 2, 3)", repr(List(1, 2, 3)))
        self.assertEqual("ListGenerator(i for i in [1, 2, 3])", repr(List(1, 2, 3).map(_*1)))

        # self.assertEqual("""List('1', '2', '3')""", repr(List("1", "2", "3")))
        # self.assertEqual("""ListGenerator(i for i in ['1', '2', '3'])""", repr(List('1', "2", '3').map(_*1)))

    def test_map(self):
        self.assertEqual(List(1, 2, 3).map(lambda x: x*2), [2, 4, 6])
        self.assertEqual(List().map(lambda x: x*2), [])
        self.assertEqual(List(1, 2, 3).map(lambda x: x*2).toList(), [2, 4, 6])
        self.assertEqual(List().map(lambda x: x*2).toList(), [])

    def test_flatten(self):
        self.assertEqual(List(1, None, 2).flatten(), [1, 2])

    def test_mkString(self):

        # self.assertEqual(List().mkString(","), "")
        self.assertEqual("1,2,3", List(1, 2, 3).mkString(","))
        # self.assertEqual(List(1,2,3).map(_ * 2).mkString(","), "1,2,3")
        self.assertEqual(List(1, 2, 3).map(lambda x: x*2).mkString(","), "2,4,6")

    def test_add(self):

        self.assertEqual([1, 2, 3, 3, 2, 1], List(1, 2, 3) ++ List(3, 2, 1))
        with self.assertRaises(TypeError):
            self.assertEqual([1, 2, 3, 3, 2, 1], List(1, 2, 3) ++(3, 2, 1))
        with self.assertRaises(TypeError):
            self.assertEqual([1, 2, 3, 3, 2, 1], List(1, 2, 3) ++[3, 2, 1])

        self.assertEqual([1, 2, 3], List(1, 2)+3)


class TestUnderscore(TestCase):

    def test_mul(self):

        self.assertEqual(["aa", "cc"], List("a", "c").map(_ * 2))
        self.assertEqual(["aa", "cc"], List("a", "c").map(2 * _))

        self.assertEqual(List(1, 2, 3).map(_ * 2), [2, 4, 6])
        self.assertEqual(List(1, 2, 3).map(3 * _), [3, 6, 9])

    def test_div(self):

        self.assertEqual(1, (_ / 2)(2))
        self.assertEqual(3, (6 / _)(2))

        self.assertEqual(List(2, 4, 6).map(_ / 2), [1, 2, 3])
        self.assertEqual(List(2, 4, 6).map(48 / _), [24, 12, 8])

        with self.assertRaises(TypeError):
            List("a").map(_ / 2)

        with self.assertRaises(TypeError):
            List("a").map(2 / _)

    def test_add(self):

        self.assertEqual(2, (1+_)(1))
        self.assertEqual(2, (_+1)(1))

        with self.assertRaises(TypeError):
            List("a").map(_ + 2)

        with self.assertRaises(TypeError):
            List("a").map(2 + _)

    def test_sub(self):

        self.assertEqual(4, (_-3)(7))
        self.assertEqual(4, (7-_)(3))

    @skip("skip test_lt")
    def test_lt(self):

        self.assertEqual(True, (_<2)(1))


    # def test_pow




