import difflib
import unittest
from time import time, sleep

from heap import Heap, heap_push_min, heap_pop_min, heap_replace_min, FileMerge, PriorityQueue, Schedule, \
    ScheduleClient, TopK


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

    def test_schedule(self):
        a_queue = PriorityQueue()
        cron = Schedule(a_queue)
        cron.start()

        cron = ScheduleClient(a_queue)
        time_ = time()
        cron.input_task(time_ + 4, 'first task', lambda x: print(f'first task at {x()}'), time)
        cron.input_task(time_ + 8, 'second task', lambda x: print(f'second task at {x()}'), time)

        sleep(1)
        cron.input_task(time_ + 2, 'insert task', lambda x: print(f'insert task  at {x()}'), time)
        print('input done')
        print()

    def test_top_K(self):
        random_num_list = [395, 236, 921, 273, 468, 146, 832, 730, 607, 775, 441, 372, 431, 44, 697, 359, 238, 108, 166,
                           914, 484, 852,
                           897, 555, 251, 685, 826, 136, 534, 932, 533, 356, 130, 396, 220, 133, 56, 499, 959, 888, 185,
                           794, 685, 782,
                           191, 743, 953, 719, 585, 875, 592, 332, 961, 399, 287, 776, 380, 29, 512, 146, 118, 757, 788,
                           313, 260, 207,
                           96, 397, 379, 344, 828, 412, 705, 63, 332, 997, 411, 216, 221, 218, 418, 701, 269, 837, 717,
                           866,
                           733, 818,
                           251, 658, 243, 8, 650, 949, 459, 694, 291, 841, 431, 161]

        top_k = TopK(random_num_list)
        top_k.init()
        list_1 = sorted(top_k.heap)
        list_2 = sorted(random_num_list)[-10:]
        self.assertListEqual(list_1, list_2)






