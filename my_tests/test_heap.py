import unittest

from heap import Heap


class TestHashMapCase(unittest.TestCase):

    def test_head_insert_and_remove_max(self):
        a = Heap(10)
        a.insert(9)
        a.insert(8)
        a.insert(5)
        a.insert(2)
        a.insert(11)
        a.insert(3)
        a.insert(99)

        self.assertEqual(99, a.remove_max_value())
        self.assertEqual(11, a.remove_max_value())
        self.assertEqual(9, a.remove_max_value())
        print(a.items)

    def test_head_build_and_sort(self):
        a = Heap(10)
        a.build_heap([9, 8, 5, 2, 11, 3, 99])
        self.assertEqual([None, 99, 11, 9, 2, 8, 3, 5], a.items)
        self.assertEqual([99, 11, 9, 8, 5, 3, 2], a.sort())
