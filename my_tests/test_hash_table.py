import unittest

from hash_table import HashMap


class TestHashMapCase(unittest.TestCase):

    def test_hash_map(self):
        map = HashMap(3)
        self.check_map(map)

    def test_hash_map_2(self):
        """插入的最后一个成员 刚好满足动态扩容
        :return:
        """
        map = HashMap(6)
        self.check_map(map)
        print(map.print_self())

    def test_hash_map_3(self):
        map = HashMap(7)
        self.check_map(map)
        del map['a']
        self.assertFalse('a' in map)

    def test_hash_map_4(self):
        map = HashMap(1)
        self.check_map(map)

    def test_hash_map_5(self):
        map = HashMap(10)
        with self.assertRaises(KeyError):
             x = map['a']

        with self.assertRaises(KeyError):
            del map['a']

    def check_map(self, map):
        map.insert('a', '1')
        map.insert('a', 'a')
        map.insert('b', '2')
        map.insert('c', '3')
        map.insert('d', '4')
        map.insert('e', '5')
        map.insert('f', '6')
        self.assertEqual(map.to_dict(), {'b': '2', 'c': '3', 'f': '6', 'd': '4', 'e': '5', 'a': 'a'})
        self.assertEqual(map['a'], 'a')
        self.assertEqual(map['b'], '2')
        self.assertEqual(map['c'], '3')
        self.assertEqual(map['d'], '4')
        self.assertEqual(map['e'], '5')
        self.assertEqual(map['f'], '6')

    def test_hash_map_6(self):
        map = HashMap(10)
        map['a'] = 3
        map['b'] = 4
        self.assertEqual(3, map['a'])
        self.assertEqual(4, map['b'])

    def test_hash_map_7(self):
        map = HashMap(10)
        map['a'] = 3
        map['b'] = 4
        self.assertEqual(3, map.pop('a'))
        self.assertEqual(1, map.pop('z', 1))
        with self.assertRaises(KeyError):
            x = map['a']

    def test_hash_map_8(self):
        map = HashMap(10)
        map['a'] = 1
        self.assertEqual(len(map), 1)
        self.assertTrue(isinstance(map.popitem(), tuple))
        self.assertEqual(len(map), 0)

    def test_hash_map_9(self):
        map = HashMap(10)
        map['a'] = 1
        x = {'a': 2, 'b': '2', 'd': 3, 'c': 3}
        map.update(x)
        self.assertEqual(x, map.to_dict())
        self.assertEqual(len(map), 4)

    def test_hash_map_10(self):
        map = HashMap(15)
        map['a'] = 1
        x = {'a': 2, 'b': '2', 'd': 3, 'c': 3}
        map.update(x)
        map.clear()
        self.assertEqual({}, map.to_dict())
        self.assertEqual(len(map), 0)

    def test_hash_map_11(self):
        pass

    def test_hash_map_12(self):
        map = HashMap.fromkeys(['q', 'w', 'e', 'r'], 'ada')
        self.assertDictEqual(dict.fromkeys(['q', 'w', 'e', 'r'], 'ada'), map.to_dict())

    def test_hash_map_13(self):
        map = HashMap()
        map['a'] = 3
        map.setdefault('a', '123')
        map.setdefault('aa', '123')
        self.assertDictEqual(dict(a=3, aa='123'), map.to_dict())


if __name__ == '__main__':
    unittest.main()
