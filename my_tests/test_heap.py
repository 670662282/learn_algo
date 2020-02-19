import unittest
import difflib

from heap import Heap, heap_push_min, heap_pop_min, heap_replace_min, FileMerge, file_name


class TestHashMapCase(unittest.TestCase):

    def test_heap_insert_and_remove_max(self):
        a = Heap(10)
        a.heap_push(9)
        a.heap_push(8)
        a.heap_push(5)
        a.heap_push(2)
        a.heap_push(11)
        a.heap_push(3)
        a.heap_push(99)

        self.assertEqual(99, a.heap_pop())
        self.assertEqual(11, a.heap_pop())
        self.assertEqual(9, a.heap_pop())
        print(a.items)

    def test_heap_build_and_sort(self):
        a = Heap(10)
        a.build_heap([9, 8, 5, 2, 11, 3, 99])
        self.assertEqual([None, 99, 11, 9, 2, 8, 3, 5], a.items)
        self.assertEqual([99, 11, 9, 8, 5, 3, 2], a.sort())

    def test_min_heap(self):
        x = []
        heap_push_min(x, 9)
        heap_push_min(x, 8)
        heap_push_min(x, 5)
        heap_push_min(x, 2)
        heap_push_min(x, 11)
        heap_push_min(x, 3)
        heap_push_min(x, 9)
        self.assertEqual([2, 5, 3, 9, 11, 8, 9], x)
        self.assertEqual(2, heap_pop_min(x))
        self.assertEqual([3, 5, 8, 9, 11, 9], x)
        self.assertEqual(3, heap_replace_min(x, 1))
        self.assertEqual([1, 5, 8, 9, 11, 9], x)

    def test_file_merge(self):
        merge = FileMerge('data')
        merge.run()
        with open('output.txt') as f_1:
            with open('expect_output.txt') as f_2:
                result = difflib.unified_diff(
                    f_1.readlines(), f_2.readlines(), fromfile='output.txt', tofile='expect_output.txt')
            if list(result):
                raise AssertionError(f'file merge file, diff: {result}')




