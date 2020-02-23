import difflib
import unittest
from heapq import heappush

from heap import Heap, heap_push_min, heap_pop_min, heap_replace_min, FileMerge, TopK, heap_push_max, heap_pop_max, \
    build_heap, heapify_max, DynamicMedian


def judge_position(length):
    """
    根据位置判断此数据应该在二叉树的第几行、第几列
    :param length:
    :return:
    """
    rows = 0

    # get rows
    while True:
        if (2 ** (rows - 1)) <= length <= (2 ** rows - 1):
            break
        else:
            rows += 1

    # get cols
    cols = length - 2 ** (rows - 1) + 1

    return rows, cols


def binary_tree_printer(list_=None):
    """
    打印列表为二叉树形状
    :param list_: 传入的列表
    :return:
    """
    rows = judge_position(len(list_))[0]  # rows为总行数
    count = 0
    pre_row, pre_col = 0, 0  # 记录上一个数的行与列

    for x in list_:
        count += 1  # 计数现在打印的是第几个数
        x_row, x_col = judge_position(count)  # 计算出当前打印的数位于第几行，第几列
        if x_row != pre_row:  # 如果换行了，那么打印换行符
            print('\n')
        if x_col != 1:  # 如果当前打印的数字不是本行第一个，则打印步长为2**(rows-x_row+1)-1
            print('  ' * (2 ** (rows - x_row + 1) - 1), end='')
        else:
            print('  ' * ((2 ** (rows - x_row + 1) - 1) // 2), end='')
        print('{0:2}'.format(x), end='')
        pre_row, pre_col = x_row, x_col  # 位置记录更新


class TestHashMapCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.random_num_list = [395, 236, 921, 273, 468, 146, 832, 730, 607, 775, 441, 372, 431, 44, 697, 359, 238, 108,
                               166,
                               914, 484, 852,
                               897, 555, 251, 685, 826, 136, 534, 932, 533, 356, 130, 396, 220, 133, 56, 499, 959, 888,
                               185,
                               794, 685, 782,
                               191, 743, 953, 719, 585, 875, 592, 332, 961, 399, 287, 776, 380, 29, 512, 146, 118, 757,
                               788,
                               313, 260, 207,
                               96, 397, 379, 344, 828, 412, 705, 63, 332, 997, 411, 216, 221, 218, 418, 701, 269, 837,
                               717,
                               866,
                               733, 818,
                               251, 658, 243, 8, 650, 949, 459, 694, 291, 841, 431, 161]

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

    def test_max_heap(self):
        x = []
        heap_push_max(x, 9)
        heap_push_max(x, 8)
        heap_push_max(x, 5)
        heap_push_max(x, 2)
        heap_push_max(x, 11)
        heap_push_max(x, 3)
        heap_push_max(x, 9)
        self.assertEqual([11, 9, 9, 2, 8, 3, 5], x)
        self.assertEqual(11, heap_pop_max(x))
        self.assertEqual([9, 8, 9, 2, 5, 3], x)

    def test_max_heap_2(self):
        x = []
        num = self.random_num_list
        for i in num:
            heap_push_max(x, i)
        xx = [997, 961, 959, 953, 949, 921, 832, 828, 914, 888, 932, 841, 875, 776, 788, 356, 397, 607, 705, 730, 866,
              818, 897, 826, 719, 685, 555, 534, 512, 395, 757, 313, 207, 379, 396, 412, 332, 499, 468, 418, 701, 794,
              837, 782, 658, 743, 852, 585, 694, 251, 592, 332, 372, 399, 287, 44, 380, 29, 136, 146, 118, 533, 697,
              236, 260, 130, 96, 238, 359, 220, 344, 108, 133, 56, 63, 166, 411, 216, 221, 218, 273, 185, 269, 484, 717,
              685, 733, 441, 251, 191, 243, 8, 650, 775, 459, 146, 291, 431, 431, 161]
        print(x)
        self.assertListEqual(x, xx)

    def _heap_push_with_start_1(self, heap, value, pos, start_pos=1):
        # 从数组 1开始
        # 自下往上堆化 Restore the heap invariant
        # 减少比较次数
        heap.append(value)
        new_item = heap[pos]

        while pos > start_pos:
            parent_pos = pos >> 1
            parent = heap[parent_pos]
            if new_item < parent:
                heap[pos] = parent
                pos = parent_pos
                continue
            break
        heap[pos] = new_item

    def _heap_push_with_start_0(self, heap, value, pos, start_pos=0):
        # 从数组 1开始
        # 自下往上堆化 Restore the heap invariant
        # 减少比较次数
        heap.append(value)
        new_item = heap[pos]

        while pos > start_pos:
            parent_pos = pos - 1 >> 1
            parent = heap[parent_pos]
            if new_item < parent:
                heap[pos] = parent
                pos = parent_pos
                continue
            break
        heap[pos] = new_item

    def test_x(self):
        x = [None]
        z = []
        y = []
        for i in self.random_num_list:
            self._heap_push_with_start_1(x, i, len(x))
            # todo _heap_push_with_start_0 error
            self._heap_push_with_start_0(z, i, len(z)-1)
            heappush(y, i)
        self.assertListEqual(x[1:], y)
        self.assertListEqual(x[1:], z)

    def test_min_heap_2(self):
        x = []
        y = []
        for i in self.random_num_list:
            heappush(y, i)
            heap_push_min(x, i)
        self.assertListEqual(x, y)

    def test_build_heap_min(self):
        x = self.random_num_list[:]
        build_heap(x)
        self.assertEqual(8, x[0])

    def test_build_heap_max(self):
        x = self.random_num_list[:]
        build_heap(x, heapify=heapify_max)
        self.assertEqual(997, x[0])

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
        """测试定时器"""
        # a_queue = PriorityQueue()
        # cron = Schedule(a_queue)
        # cron.start()
        #
        # cron = ScheduleClient(a_queue)
        # time_ = time()
        # cron.input_task(time_ + 4, 'first task', lambda x: print(f'first task at {x()}'), time)
        # cron.input_task(time_ + 8, 'second task', lambda x: print(f'second task at {x()}'), time)
        #
        # sleep(1)
        # cron.input_task(time_ + 2, 'insert task', lambda x: print(f'insert task  at {x()}'), time)
        # print('input done')
        # print()

    def test_top_K(self):
        nums = self.random_num_list[:]
        top_k = TopK(nums)
        top_k.init()
        list_1 = sorted(top_k.heap)
        list_2 = sorted(nums)[-10:]
        self.assertListEqual(list_1, list_2)

    def test_median(self):
        nums = [6, 4, 1, 2, 3, 7]
        dy = DynamicMedian()
        dy.init(nums)
        self.assertEqual(3, dy.value)

        for i in self.random_num_list:
            dy.insert(i)

        self.assertTrue(
            abs(len(dy.min_heap) - len(dy.max_heap)) == 1 or
            len(dy.min_heap) - len(dy.max_heap) == 0
        )
        binary_tree_printer(dy.min_heap)
        binary_tree_printer(dy.max_heap)
        self.assertEqual(412, dy.value)

    def test_median_2(self):
        nums = self.random_num_list[:]
        dy = DynamicMedian(n=0.9)
        dy.init(nums)

        for i in range(1000):
            dy.insert(i)

        print(dy.min_heap)
        print(dy.max_heap)
        self.assertEqual(897, dy.value)
