import math
import os
import threading
from time import time

from my_queue import BlockQueue

"""小堆
从数组0开始
a[i] <= a[2*i+1] and a[i] <= a[2*i+2]  父节点就是下标为  i // 2  -1的节点

"""


def swap(list_, pos_a, pos_b):
    list_[pos_a], list_[pos_b] = list_[pos_b], list_[pos_a]


def _heap_down_min(heap, pos, start_pos=0):
    # 自下往上堆化 Restore the heap invariant
    # 减少比较次数
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


def heap_push_min(heap: list, item):
    heap.append(item)
    _heap_down_min(heap, len(heap)-1)


def heap_pop_min(heap):
    last = heap.pop()

    if heap:
        result = heap[0]
        heap[0] = last
        heapify_min(heap)
        return result
    return last


def heap_replace_min(heap, item):
    """ heap pop and push"""
    result = heap[0]
    heap[0] = item
    heapify_min(heap)
    return result


def heapify_min(heap, start_pos: int = 0):
    """从上往下堆化"""
    size = len(heap)
    while True:
        left_child_pos = start_pos * 2 + 1
        right_child_pos = left_child_pos + 1

        min_pos = start_pos
        if left_child_pos < size and heap[left_child_pos] < heap[start_pos]:
            min_pos = left_child_pos

        if right_child_pos < size and heap[right_child_pos] < heap[min_pos]:
            min_pos = right_child_pos

        if min_pos == start_pos:
            break
        swap(heap, min_pos, start_pos)
        start_pos = min_pos


"""大堆
从数组0开始
"""


def _heap_up_max(heap, pos, start_pos: int = 0):
    # 自下往上堆化 Restore the heap invariant
    new_item = heap[pos]

    while pos > start_pos:
        parent_pos = pos - 1 >> 1
        parent = heap[parent_pos]

        if new_item > parent:
            heap[pos] = parent
            pos = parent_pos
            continue
        break
    heap[pos] = new_item


def heap_pop_max(heap):
    last = heap.pop()

    if heap:
        result = heap[0]
        heap[0] = last
        heapify_max(heap)
        return result
    return last


def heap_push_max(heap, value):
    heap.append(value)
    _heap_up_max(heap, len(heap)-1)


def heapify_max(heap, start_pos: int = 0):
    """从上往下堆化"""
    size = len(heap)
    while True:
        left_child_pos = start_pos * 2 + 1
        right_child_pos = left_child_pos + 1

        max_pos = start_pos
        if left_child_pos < size and heap[start_pos] < heap[left_child_pos]:
            max_pos = left_child_pos

        if right_child_pos < size and heap[max_pos] < heap[right_child_pos]:
            max_pos = right_child_pos

        if max_pos == start_pos:
            break
        swap(heap, max_pos, start_pos)
        start_pos = max_pos


def build_heap(items: list, heapify=heapify_min):
    """建堆 默认小堆
    从后往前处理数组
    从非叶子节点开始(倒数第二层) 从上往下堆化
    heapify: 堆化函数
    """
    if len(items) < 2:
        return
    current = len(items) // 2
    while current >= 0:
        heapify(items, current)
        current -= 1


class Heap:
    """大堆 基于数组实现
    基于数组1开始的
    a[i] <= a[2*i] and a[i] <= a[2*i+1]
    数组中下标为 i 的节点的左子节点，就是下标为 i∗2 的节点，右子节点就是下标为 i∗2+1 的节点，父节点就是下标为 i // 2​的节点。
    """

    def __init__(self, capacity):
        self.items = [None] * (capacity + 1)
        self.count = 0
        self.__top_pos = 1  # head top pos

    def __len__(self):
        return self.count

    def __repr__(self):
        return self.items[:self.count + 1]

    def __swap(self, a: int, b: int):
        self.items[b], self.items[a] = self.items[a], self.items[b]

    def heap_push(self, value):
        if self.count > len(self.items):
            return
        self.count += 1
        self.items[self.count] = value
        current = self.count
        self._heap_up(current)

    def _heap_up(self, current):
        # 自下往上堆化 Restore the heap invariant
        while current // 2 >= self.__top_pos and self.items[current] > self.items[current // 2]:
            # 交换
            self.__swap(current // 2, current)
            current = current // 2

    def heap_pop(self):
        if self.count == 0:
            print('items count is 0')
            return None
        print(f'items: {self.__repr__()}')

        result = self.items[self.__top_pos]
        self.items[self.__top_pos] = self.items[self.count]
        # self.__swap(self.__top_pos, self.count)
        self.count -= 1
        self.heapify()
        print(f'remove max value is {result}')
        print(f'items: {self.__repr__()}')
        print()
        return result

    def father_pos(self, i):
        if i // 2 < self.__top_pos:
            return None
        return i // 2

    def left_child_pos(self, i):
        if i * 2 > self.count:
            return None
        return i * 2

    def right_child_pos(self, i):
        if i * 2 + 1 > self.count:
            return None
        return i * 2 + 1

    def heap_replace(self, item):
        result = self.items[1]
        self.items[1] = item
        self.heapify()
        return result

    def heapify(self, start_pos: int = None):
        """自上往下堆化
        """
        if start_pos is None:
            max_pos = current_pos = self.__top_pos
        else:
            if start_pos < self.__top_pos:
                print(f'{start_pos} < self.__top_pos')
                return
            max_pos = current_pos = start_pos

        while True:
            left_pos = self.left_child_pos(current_pos)
            right_pos = self.right_child_pos(current_pos)

            # if current < left child, swap current, left child

            if left_pos is not None and self.items[current_pos] < self.items[left_pos]:
                max_pos = left_pos

            # if max_pos < right child , swap max_pos, right child
            if right_pos is not None and self.items[max_pos] < self.items[right_pos]:
                max_pos = right_pos

            if max_pos == current_pos:
                break
            # 交换
            self.__swap(max_pos, current_pos)
            current_pos = max_pos

    def build_heap(self, items: list):
        """items index0为空的数组
        """
        self.items = [None] + items
        self.count = len(items)

        # 对下标从 len(self.items) // 2​ 开始到 1 的数据进行堆化
        current = len(self.items) // 2
        # 从非叶子节点开始 从上往下堆化
        while current >= self.__top_pos:
            self.heapify(current)
            current -= 1

    def sort(self, reverse=False):
        """数组中的第一个元素就是堆顶，也就是最大的元素。我们把它跟最后一个元素交换，那最大元素就放到了下标为 n 的位置。 """
        item_bak = self.items[:]
        count_bak = self.count
        result = [None] * (len(self.items) - 1)

        if reverse:
            for index in range(len(result) - 1, -1, -1):
                result[index] = self.heap_pop()
        else:
            for index in range(len(result)):
                result[index] = self.heap_pop()

        self.items = item_bak
        self.count = count_bak
        return result


"""
堆的应用一 合并100个有序小文件 到一个有序大文件
"""


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        print('root_dir:', root)  # 当前目录路径
        print('sub_dirs:', dirs)  # 当前路径下所有子目录
        print('files:', files)  # 当前路径下所有非目录子文件
        return files


class FileMerge:
    """
    这里就可以用到优先级队列，也可以说是堆。我们将从小文件中取出来的字符串放入到小顶堆中，
    那堆顶的元素，也就是优先级队列队首的元素，就是最小的字符串。
    我们将这个字符串放入到大文件中，并将其从堆中删除。
    然后再从小文件中取出下一个字符串，放入到堆中。
    循环这个过程，就可以将 100 个小文件中的数据依次放入到大文件中。
    """

    def __init__(self, file_dir):
        self.file_dir = file_dir
        self.file_list = file_name(file_dir)
        self.heap = []

    def run(self, out_put_file='output.txt'):
        for file in self.file_list:
            path = os.path.join(self.file_dir, file)
            with open(path) as f:
                heap_push_min(self.heap, (f.read(1), path))

        self._merge(out_put_file)

    def _merge(self, out_put_file):
        with open(out_put_file, 'w') as f_w:
            for index, file in self.heap:
                with open(file) as f_r:
                    for line in f_r:
                        f_w.write(line)


"""
简单定时器
每过 1 秒就扫描一遍任务列表的做法比较低效，
主要原因有两点：第一，任务的约定执行时间离当前时间可能还有很久，这样前面很多次扫描其实都是徒劳的；
第二，每次都要扫描整个任务列表，如果任务列表很大的话，势必会比较耗时。

针对这些问题，我们就可以用优先级队列来解决。我们按照任务设定的执行时间，将这些任务存储在优先级队列中
，队列首部（也就是小顶堆的堆顶）存储的是最先执行的任务。这样，定时器就不需要每隔 1 秒就扫描一遍任务列表了。
它拿队首任务的执行时间点，与当前时间点相减，得到一个时间间隔 T。这个时间间隔 T 就是，从当前时间开始，需要等待多久，
才会有第一个任务需要被执行。这样，定时器就可以设定在 T 秒之后，再来执行任务。从当前时间点到（T-1）秒这段时间里，
定时器都不需要做任何事情。当 T 秒时间过去之后，定时器取优先级队列中队首的任务执行。
然后再计算新的队首任务的执行时间点与当前时间点的差值，把这个值作为定时器执行下一个任务需要等待的时间
"""

event = threading.Event()


class PriorityQueue(BlockQueue):
    def _init(self, maxsize):
        self._queue = []

    def _append(self, item):
        heap_push_min(self._queue, item)

    def _pop_left(self):
        return heap_pop_min(self._queue)

    def _qsize(self):
        return len(self._queue)

    def top(self):
        if not self.empty():
            return self._queue[0]


class Schedule(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.remain_time = None

    def parse_task(self):
        """查看队首任务的执行时间点，与当前时间点相减，得到一个时间间隔 T，这段时间点将阻塞
        如果唤醒后（每次队列首任务变化了也会唤醒），再次查看查看队首任务的执行时间点，是不是当前任务，如果是，则返回这个task

        如果不是，则重复
        """
        while True:
            if not self.queue.empty():
                break

        while True:
            task = self.queue.top()
            remain_time = task[0] - time()
            if remain_time > 0.0:
                # print(f'{task[1]} wait {remain_time} ')
                event.wait(remain_time)

            # 唤醒后， 如果没有新任务插入则返回
            if task == self.queue.top():
                return self.queue.get()
            else:
                print('队列首变化事件处理完成')
                event.clear()

    def run(self):
        print("开启线程：")
        while True:
            task = self.parse_task()
            print(task)
            print()
            task[2](*task[3], **task[4])


class ScheduleClient:
    def __init__(self, queue):
        self.queue = queue

    def input_task(self, task_time, fun_name, func, *args, **kwargs):
        if time() > task_time:
            raise ValueError('delay_time is elapsed time')

        if not callable(func):
            raise ValueError('fun must be callable')

        if self.queue.top() and task_time < self.queue.top()[0]:
            print('发生队列首变化事件，唤醒线程')
            event.set()
        self.queue.put_nowait((task_time, fun_name, func, args, kwargs))


class TopK:
    """
    求 Top K 的问题抽象成两类。
    一类是针对静态数据集合，也就是说数据集合事先确定，不会再变。
    另一类是针对动态数据集合，也就是说数据集合事先并不确定，有数据动态地加入到集合中。

    针对静态数据，如何在一个包含 n 个数据的数组中，查找前 K 大数据呢？

    我们可以维护一个大小为 K 的小顶堆，顺序遍历数组，从数组中取出数据与堆顶元素比较。
    如果比堆顶元素大，我们就把堆顶元素删除，并且将这个元素插入到堆中；如果比堆顶元素小，则不做处理，继续遍历数组。
    这样等数组中的数据都遍历完之后，堆中的数据就是前 K 大数据了。

    遍历数组需要 O(n) 的时间复杂度，一次堆化操作需要 O(logK) 的时间复杂度，所以最坏情况下，n 个元素都入堆一次，时间复杂度就是 O(nlogK)。

    针对动态数据求得 Top K 就是实时 Top K
    如果每次询问前 K 大数据，我们都基于当前的数据重新计算的话，那时间复杂度就是 O(nlogK)，n 表示当前的数据的大小。
    实际上，我们可以一直都维护一个 K 大小的小顶堆，当有数据被添加到集合中时，我们就拿它与堆顶的元素对比。
    如果比堆顶元素大，我们就把堆顶元素删除，并且将这个元素插入到堆中；
    如果比堆顶元素小，则不做处理。这样，无论任何时候需要查询当前的前 K 大数据，我们都可以立刻返回给他。
    """

    def __init__(self, big_nums_list, k=10):
        self.big_nums_list = big_nums_list
        self.k = k
        self.heap = []

    def init(self):
        for i in self.big_nums_list[:self.k]:
            heap_push_min(self.heap, i)

        for i in self.big_nums_list[self.k:]:
            self.update(i)

    def update(self, num):
        if num > self.heap[0]:
            heap_replace_min(self.heap, num)


class DynamicMedian:
    """
    对于一组静态数据，中位数是固定的，我们可以先排序，第 2n​ 个数据就是中位数。
    每次询问中位数的时候，我们直接返回这个固定的值就好了。所以，尽管排序的代价比较大，但是边际成本会很小。
    但是，如果我们面对的是动态数据集合，中位数在不停地变动，如果再用先排序的方法，每次询问中位数的时候，都要先进行排序，那效率就不高了
    借助堆这种数据结构，我们不用排序，就可以非常高效地实现求中位数操作

    我们需要维护两个堆，一个大顶堆，一个小顶堆。大顶堆中存储前半部分数据，小顶堆中存储后半部分数据，且小顶堆中的数据都大于大顶堆中的数据。
    如果有 n 个数据，n 是偶数，我们从小到大排序，
    那前 2/n​ 个数据存储在大顶堆中，后 2/n​ 个数据存储在小顶堆中。
    这样，大顶堆中的堆顶元素就是我们要找的中位数。
    如果 n 是奇数，情况是类似的，大顶堆就存储 2/n​+1 个数据，小顶堆中就存储 2/n​ 个数据

    当新添加一个数据的时候，我们如何调整两个堆，让大顶堆中的堆顶元素继续是中位数呢？
    如果新加入的数据小于等于大顶堆的堆顶元素，我们就将这个新数据插入到大顶堆；否则，我们就将这个新数据插入到小顶堆。
    """

    def __init__(self, n=0.5):
        self.n = n
        self.max_heap = []  # 存储 前部分 nums_len * n
        self.min_heap = []  # 存储 后部分 nums_len * （1-n）

    def init(self, data_list):
        data = sorted(data_list)
        # 向上取整 如果是奇数 则大顶堆多存一个
        value = self.split_value(len(data))
        self.max_heap = data[:value]
        self.min_heap = data[value:]
        build_heap(self.max_heap, heapify=heapify_max)
        build_heap(self.min_heap)

    def split_value(self, count):
        if self.n <= 0 or self.n >= 1:
            raise ValueError('n must > 0 and <1')
        return math.ceil(count * self.n)

    @property
    def value(self):
        return self.max_heap[0]

    def __len__(self):
        return len(self.max_heap) + len(self.min_heap)

    def insert(self, num):

        if len(self.min_heap) == 0 or len(self.max_heap) == 0:
            raise ValueError('must init')

        if num > self.max_heap[0]:
            heap_push_min(self.min_heap, num)
        else:
            heap_push_max(self.max_heap, num)

        # 两个堆中的数据个数不符合前面约定的情况 我们可以从一个堆中不停地将堆顶元素移动到另一个堆
        value = self.split_value(self.__len__())
        print(f'split value: {value}')
        if len(self.max_heap) > value:
            self.move_to_min_heap()
            return

        if len(self.max_heap) < value:
            self.move_to_max_heap()
            return

    def move_to_min_heap(self):
        """大堆 堆顶 移动到小堆
        """
        # print(f'move_to_min_heap')
        value = heap_pop_max(self.max_heap)
        heap_push_min(self.min_heap, value)

    def move_to_max_heap(self):
        """小堆 堆顶 移动到大堆
        """
        # print(f'move_to_max_heap')
        value = heap_pop_min(self.min_heap)
        heap_push_max(self.max_heap, value)


if __name__ == '__main__':
    #nums = [6, 4, 1, 2, 3, 7]
    nums = [395, 236, 921, 273, 468, 146, 832, 730, 607, 775, 441, 372, 431, 44, 697, 359, 238, 108, 166,
            914, 484, 852,
            897, 555, 251, 685, 826, 136, 534, 932, 533, 356, 130, 396, 220, 133, 56, 499, 959, 888, 185,
            794, 685, 782,
            191, 743, 953, 719, 585, 875, 592, 332, 961, 399, 287, 776, 380, 29, 512, 146, 118, 757, 788,
            313, 260, 207,
            96, 397, 379, 344, 828, 412, 705, 63, 332, 997, 411, 216, 221, 218, 418, 701, 269, 837, 717,
            866,
            733, 818,
            251, 658, 243, 8, 650, 949, 459, 694, 291, 841, 431, 161]
    dy = DynamicMedian()
    dy.init(nums)
    print(dy.min_heap)
    print(dy.max_heap)

    dy.insert(33)
    dy.insert(0)
    dy.insert(2)
    print(f'min_heap: {dy.min_heap}')
    print(f'max_heap: {dy.max_heap}')
