from unittest import TestCase, skip

from scalafn import List, _
from scalafn import fn


class Inner():
    def __init__(self, a=None):
        self.a = a

    def get_a(self):
        return self.a

    def set_a(self, a):
        self.a = a

    def set_and_get(self, a):
        return a

    def __eq__(self, other):
        return self.a == other.a





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

        #test no error raised
        List("a").map(_ / 2)
        List("a").map(2 / _)

        #assert raised
        with self.assertRaises(TypeError):
            List("a").map(_ / 2).toList()

        with self.assertRaises(TypeError):
            List("a").map(2 / _).toList()

    def test_add(self):

        self.assertEqual(2, (1+_)(1))
        self.assertEqual(2, (_+1)(1))

        with self.assertRaises(TypeError):
            List("a").map(_ + 2).toList()

        with self.assertRaises(TypeError):
            List("a").map(2 + _).toList()

    def test_sub(self):

        self.assertEqual(4, (_-3)(7))
        self.assertEqual(4, (7-_)(3))

    def test_lt(self):

        self.assertEqual(True, (_<2)(1))
        self.assertEqual(False, (2<_)(1))

    def test_le(self):

        self.assertEqual(True, (_<=2)(1))
        self.assertEqual(True, (_<=2)(2))
        self.assertEqual(False, (2<=_)(1))
        self.assertEqual(True, (2<=_)(2))

    def test_gt(self):

        self.assertEqual(True, (_>2)(3))
        self.assertEqual(False, (2>_)(3))

    def test_ge(self):

        self.assertEqual(True, (_>=2)(2))
        self.assertEqual(True, (_>=2)(3))
        self.assertEqual(False, (2>=_)(3))
        self.assertEqual(True, (2>=_)(1))

    def test_no_param(self):

        self.assertEqual([1, 2], List(1, '', 2, None, 0).filter(_))

    def test_len(self):

        self.assertEqual(0, List().length())
        self.assertEqual(0, len(List()))
        self.assertEqual(0, len(List().toStream()))
        self.assertEqual(0, List().toStream().length())

        self.assertEqual(2, List(1, 2).length())
        self.assertEqual(2, len(List(1, 2)))
        self.assertEqual(2, len(List(1, 2).toStream()))
        self.assertEqual(2, List(1, 2).toStream().length())


class TestUnderscoreAttributes(TestCase):

    def setUp(self):
        C = Inner
        self.list = List(C(1), C(2), C(3))

    def test_methods(self):

        self.assertEqual([1, 2, 3], self.list.map(_.a * 1))
        self.assertEqual([1, 2, 3], self.list.map(1 * _.a))

        self.assertEqual([1, 2, 3], self.list.map(_.a / 1))
        self.assertEqual([6, 3, 2], self.list.map(6 / _.a))





@skip('')
class TestUnderscoreAttributesCall(TestCase):

    def setUp(self):
        self.Inner = Inner

    def test_call_undefined_properties(self):

        Inner = self.Inner

        self.assertEqual(Inner(True), Inner(True))

        init = List(Inner(True), Inner(False))

        # print(List(*init).filter(_.a).toList().length())
        # print(List(Inner(False)).filter(_.a).toList())

        # print(List(*init).filter(_.a).toList().length())

        # self.assertEqual(List(Inner(True)), List(*init).filter(_.a).toList())

        # with self.assertRaises(TypeError):
        #     self.assertEqual(List(Inner(True)), List(*init).filter(_.a == True).toList())

    @skip('in feature versions')
    def test_call_undefined_methods_1(self):

        Inner = self.Inner

        init = List(Inner(1), Inner(2))

        # self.assertEqual(1, _.get_a().get_callable(Inner(1)))
        self.assertEqual(List(Inner(2)), List(*init).filter(_.get_a() > 1).toList())
        # self.assertEqual(List(Inner(2)), List(*init).filter(fn.eq(_.get_a(), 2)).toList())
        self.assertEqual(List(Inner(1), Inner(True)), List(Inner(1), Inner(True)).filter(fn.isinstance(_.get_a(), int)).toList())


    def test_call_undefined_methods_cmp(self):
        Inner = self.Inner

        # print( List(Inner(1)).map(_.get_a() > 0).toList())
        # print(List(True) == List(1))

        self.assertEqual(List(True), List(Inner(1)).map(_.get_a() > 0))
        self.assertEqual(List(True), List(Inner(2)).map(_.get_a() >= 0))
        self.assertEqual(List(False), List(Inner(3)).map(_.get_a() <= 1))
        self.assertEqual(List(False), List(Inner(3)).map(_.get_a() < 2))

    def test_call_undefined_mul(self):
        Inner = self.Inner

        self.assertEqual(List(2), List(Inner(1)).map(_.get_a() * 2))
        self.assertEqual(List(2), List(Inner(1)).map(2 * _.get_a()))

    def test_div(self):
        Inner = self.Inner

        self.assertEqual(List(1), List(Inner(2)).map(_.get_a() / 2))
        self.assertEqual(List(1), List(Inner(2)).map(2 / _.get_a()))









