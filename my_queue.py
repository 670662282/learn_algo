import threading
from queue import Empty, Full
from time import time

from heap import heap_push_min, heap_pop_min


class MyQueue:
    def __init__(self, maxsize=20):
        self.maxsize = maxsize
        self.head = 0
        self.tail = 0
        self.size = 0  # size 可以去掉
        self.items = [None] * maxsize

    def __len__(self):
        return self.size

    def _full(self):
        return self.size == len(self.items)

    def empty(self):
        if self.head == self.tail:
            return True

    def append(self, item):
        if self._full():
            return
        self.items[self.tail] = item
        self.tail += 1
        if self.tail > len(self.items):
            self.tail = 0
        self.size += 1

    def pop_left(self):
        if self.empty():
            return Empty
        result = self.items[self.head]
        self.size -= 1
        self.head += 1
        return result


class BlockQueue:
    """简单阻塞队列实现"""
    _queue = None

    def __init__(self, maxsize=20):
        self.maxsize = maxsize
        self._init(maxsize)

        self.lock = threading.Lock()
        self.no_empty = threading.Condition(self.lock)
        self.no_full = threading.Condition(self.lock)

    def empty(self):
        """ Return True if the queue is empty, False otherwise (not reliable!). """
        with self.lock:
            return not self._qsize()

    def full(self):
        """Return True if the queue is full, False otherwise (not reliable!).

        This method is likely to be removed at some point.  Use qsize() >= n
        as a direct substitute, but be aware that either approach risks a race
        condition where a queue can shrink before the result of full() or
        qsize() can be used.
        """
        with self.lock:
            if self._qsize() >= self.maxsize > 0:
                return Full

    def get(self, block=True, timeout=None):  # real signature unknown
        """
        Remove and return an item from the queue.

        If optional args 'block' is true and 'timeout' is None (the default),
        block if necessary until an item is available. If 'timeout' is
        a non-negative number, it blocks at most 'timeout' seconds and raises
        the Empty exception if no item was available within that time.
        Otherwise ('block' is false), return an item if one is immediately
        available, else raise the Empty exception ('timeout' is ignored
        in that case).
        """
        with self.no_empty:
            self._check(timeout)
            if block:
                if timeout:
                    end_time = time() + timeout
                    while not self.empty():
                        remain_time = end_time - time()
                        if remain_time <= 0.0:
                            raise Empty
                        self.no_empty.wait(remain_time)
                else:
                    while not self._qsize():
                        self.no_empty.wait()

            result = self._queue.pop_left()
            self.no_full.notify()
            return result

    def _check(self, timeout):
        if timeout < 0:
            raise ValueError("'timeout' must be a non-negative number")

    def get_nowait(self):  # real signature unknown
        """
        Remove and return an item from the queue without blocking.

        Only get an item if one is immediately available. Otherwise
        raise the Empty exception.
        """
        return self.get(block=False)

    def put(self, item, block=True, timeout=None):  # real signature unknown
        """
        Put the item on the queue.

        The optional 'block' and 'timeout' arguments are ignored, as this method
        never blocks.  They are provided for compatibility with the Queue class.
        """
        with self.no_full:
            self._check(timeout)
            if block:
                if timeout:
                    end_time = time() + timeout
                    while self.full():
                        remain_time = end_time - timeout
                        if remain_time <= 0.0:
                            raise Full
                        self.no_full.wait(remain_time)
                else:
                    while self.full():
                        self.no_full.wait()

            self._append(item)
            self.no_empty.notify()

    def put_nowait(self, item):  # real signature unknown
        """
        Put an item into the queue without blocking.

        This is exactly equivalent to `put(item)` and is only provided
        for compatibility with the Queue class.
        """
        self.put(item, block=False)

    def _init(self, maxsize):
        self._queue = MyQueue(maxsize)

    def _append(self, item):
        self._queue.append(item)

    def _pop_left(self):
        return self._queue.pop_left()

    def _qsize(self):
        """ Return the approximate size of the queue (not reliable!). """
        return len(self._queue)


class PriorityQueue(BlockQueue):
    """优先级队列应用场景非常多, 堆和优先级队列非常相似。一个堆就可以看作一个优先级队列。
    很多时候，它们只是概念上的区分而已。
    往优先级队列中插入一个元素，就相当于往堆中插入一个元素；
    从优先级队列中取出优先级最高的元素，就相当于取出堆顶元素
    """

    def _init(self, maxsize):
        self._queue = []

    def _append(self, item):
        heap_push_min(self._queue, item)

    def _pop_left(self):
        return heap_pop_min(self._queue)

    def _qsize(self):
        return len(self._queue)

