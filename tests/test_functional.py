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

class TestListFunctional(TestCase):

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

    def test_flatten(self):
        self.assertEqual(List(1, None, 2).flatten(), [1, 2])
        self.assertEqual(List(1, None, 2).toStream().flatten(), [1, 2])

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

    def test_filter(self):

        self.assertEqual([1], List(1, 2, 3).filter(_ < 2))
        self.assertEqual([1], List(1, 2, 3).toStream().filter(_ < 2))

    def test_filterNot(self):

        # self.assertEqual([0, '', False], List(*[0, 1, 2, '', True, False]).filterNot(lambda x: x))
        # self.assertEqual([0, '', False], List(*[0, 1, 2, '', True, False]).filterNot(_))

        # self.assertEqual([0, '', False], List(*[0, 1, 2, '', True, False]).toStream().filterNot(lambda x: x))
        # self.assertEqual([0, '', False], List(*[0, 1, 2, '', True, False]).toStream().filterNot(_))

        # self.assertEqual([2, 3], List(1, 2, 3).filterNot(_ < 2))
        # self.assertEqual([2, 3], List(1, 2, 3).toStream().filterNot(_ < 2))

        self.assertEqual([Inner()], List(Inner(), Inner(2), Inner(3)).filterNot(_.a).toList())
        self.assertEqual([Inner()], List(Inner(), Inner(2), Inner(3)).toStream().filterNot(_.a))

        # self.assertEqual([Inner(2), Inner(3)], List(Inner(1), Inner(2), Inner(3)).filterNot(_.a < 2))
        # self.assertEqual([Inner(2), Inner(3)], List(Inner(1), Inner(2), Inner(3)).toStream().filterNot(_.a < 2))


    def test_no_side_effect(self):

        init = [1, 2, 3]
        List(*init).map(_*2).filter(_ > 0).flatten().toList()
        self.assertEqual([1, 2, 3], init)


    def test_iterable(self):

        iter(List(1,2,3))
        iter(List(1,2,3).toStream())



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

    def test_in(self):

        self.assertTrue((_.contains(2))([1, 2, 3]))
        self.assertTrue((_.in_([1, 2, 3]))(2))

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

        self.assertEqual(List(Inner(True)), List(*init).filter(_.a).toList())

        with self.assertRaises(TypeError):
            self.assertEqual(List(Inner(True)), List(*init).filter(_.a == True).toList())

    def test_call_undefined_methods_1(self):

        Inner = self.Inner

        init = List(Inner(1), Inner(2))

        self.assertEqual(1, _.get_a()(Inner(1)))
        self.assertEqual(List(Inner(2)), List(*init).filter(_.get_a() > 1).toList())
        self.assertEqual(List(Inner(2)), List(*init).filter(fn.eq(_.get_a(), 2)).toList())
        self.assertEqual(List(Inner(1), Inner(True)), List(Inner(1), Inner(True)).filter(fn.isinstance(_.get_a(), int)).toList())

    def test_call_undefined_methods_2(self):

        Inner = self.Inner

        self.assertEqual(List(1), List(Inner()).map(_.set_and_get(a=1)).toList())
        self.assertEqual(List(1), List(Inner()).map(_.set_and_get(1)).toList())
        self.assertEqual(List(2), List(Inner()).map(_.set_and_get(2)).toList())
        with self.assertRaises(TypeError):
            self.assertEqual(List(2), List(Inner()).map(_.get_a(b=2)).toList())

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




class TestFunctions(TestCase):

    def test_isinstance(self):

        # isinstance = underscore_wrapper(isinstance)
        self.assertTrue(fn.isinstance(_, int)(1))
        self.assertTrue(fn.isinstance(1, _)(int))
        self.assertEqual([1, 2], List(1, 2, '3').filter(fn.isinstance(_, int)))

    def test_len(self):

        self.assertEqual(10, fn.len([1]*10))
        self.assertEqual(0, fn.len(_)([]))
        self.assertEqual(10, fn.len(_)([1]*10))
        self.assertEqual([1, 2, 3], List([1], [1, 1], [1, 1, 1]).map(len))
        self.assertEqual([1, 2, 3], List([1], [1, 1], [1, 1, 1]).map(fn.len))
        #
        self.assertEqual([0, 1, 2], List("", "2", "33").toStream().map(len))
        self.assertEqual([0, 1, 2], List("", "2", "33").toStream().map(fn.len))
        self.assertEqual([0, 1, 2], List("", "2", "33").toStream().map(fn.len(_)))

        self.assertEqual(['1'], List('1', '').filter(fn.len))

    def test_eq(self):

        self.assertTrue(fn.eq(1, 1))
        self.assertTrue(fn.eq(_, 1)(1))
        self.assertTrue(fn.eq(1, _)(1))
        self.assertEqual([True, False], List(1, 2).map(fn.eq(_, 1)))
        self.assertEqual([1, 2, 3], List([1], [1, 1], [1, 1, 1]).map(fn.len))
        #
        self.assertEqual([True], List("", "2", "33").toStream().map(fn.eq(_, "")).flatten())
        self.assertEqual([True], List("", "2", "33").map(fn.eq(_, "")).flatten())
        self.assertEqual([True], List("", "2", "33").toStream().map(fn.eq("", _)).flatten())





