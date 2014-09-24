from unittest import TestCase
from fn.monad import Option
from scalafn import List, Map


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

    def test_sorted(self):

        self.assertEqual(List(3, 1, 2).sorted(), [1, 2, 3])
        self.assertEqual(List(3, 1, 2).toStream().sorted(), [1, 2, 3])
        self.assertEqual(List(3, 1, 2).sorted(key=lambda x: x), [1, 2, 3])
        self.assertEqual(List(3, 1, 2).sorted(key=lambda x: x, reverse=True), [3, 2, 1])

    def test_call_optionable(self):

        self.assertIsInstance(List(1,2)(0), Option)
        self.assertIsInstance(List(1,2)(10), Option)

        self.assertEqual(List(1, 2)(0).get_or(0), 1)
        self.assertEqual(List(1, 2).toStream()(3).get_or(10), 10)

    def test_to_set(self):

        s1 = set(List('1', '2', '3'))
        self.assertEqual(s1, {'1', '2', '3'})

        s2 = set(List('1', '2', '3').toStream())
        self.assertEqual(s2, {'1', '2', '3'})


    def test_partition(self):

        s1 = List("1", "a", "2", "b", "3")
        self.assertEqual((List("1", "2", "3"), List("a", "b")), s1.partition(lambda x: x.isdigit()))
        self.assertEqual((List("1", "2", "3"), List("a", "b")), s1.toStream().partition(lambda x: x.isdigit()))

    def test_to_map(self):

        s1 = List(1, 2, 3, 4)

        self.assertEqual(Map([(1, 2), (2, 3), (3, 4), (4, 5)]), s1.toMap(lambda x: (x, x+1)))
        self.assertEqual(Map([(1, 2), (2, 3), (3, 4), (4, 5)]), s1.toStream().toMap(lambda x: (x, x+1)))

        self.assertEqual(Map([(1, 2), (2, 3), (3, 4), (4, 5)]), s1.to_map(lambda x: (x, x+1)))
        self.assertEqual(Map([(1, 2), (2, 3), (3, 4), (4, 5)]), s1.toStream().to_map(lambda x: (x, x+1)))

    def test_true(self):

        s1 = List(1, "2", None, False, "")

        self.assertEqual(List(1, "2"), s1.true())
        self.assertEqual(List(1, "2"), s1.toStream().true())

    def test_false(self):

        s1 = List(1, "2", None, False, "")

        self.assertEqual(List(None, False, ""), s1.false())
        self.assertEqual(List(None, False, ""), s1.toStream().false())

    def test_example1(self):
        str1 = """blablabla@yandex.ru R=dnslookup T=remote_smtp H=mx.yandex.ru [127.0.0.1] X=TLS1.0:RSA_AES_256_CBC_SHA1:32"""
        str2 = """<> R=1XSUTD-0008L9-Vn U=Debian-exim P=local S=5035 T="Mail delivery failed: returning message to sender" for noreply@example.com"""
        import re

        rs1 = List(*re.split(" (?=\w=)", str1)).filter(lambda x: x.count("=")).toMap(lambda x: x.split("=", 1))
        self.assertEqual(dict(
            R='dnslookup',
            T='remote_smtp',
            H='mx.yandex.ru [127.0.0.1]',
            X='TLS1.0:RSA_AES_256_CBC_SHA1:32'
        ), rs1)

        rs2 = List(*re.split(" (?=\w=)", str2)).filter(lambda x: x.count("=")).toMap(lambda x: x.split("=", 1))
        self.assertEqual(dict(
            R='1XSUTD-0008L9-Vn',
            U='Debian-exim',
            P='local',
            S='5035',
            T='"Mail delivery failed: returning message to sender" for noreply@example.com'
        ), rs2)
        