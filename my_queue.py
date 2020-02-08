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
        if self.tail > self.size:
            self.tail = 0
        self.size += 1

    def pop_left(self):
        if self.empty():
            return None
        self.size -= 1
        result = self.items[self.head]
        self.head += 1
        return result


class BlockQueue:
    """简单阻塞队列实现"""

    def __init__(self, maxsize=20):
        self.maxsize = maxsize

    def empty(self):  # real signature unknown
        """ Return True if the queue is empty, False otherwise (not reliable!). """
        pass

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
        pass

    def get_nowait(self):  # real signature unknown
        """
        Remove and return an item from the queue without blocking.

        Only get an item if one is immediately available. Otherwise
        raise the Empty exception.
        """
        pass

    def put(self, item, block=True, timeout=None):  # real signature unknown
        """
        Put the item on the queue.

        The optional 'block' and 'timeout' arguments are ignored, as this method
        never blocks.  They are provided for compatibility with the Queue class.
        """
        pass

    def put_nowait(self, item):  # real signature unknown
        """
        Put an item into the queue without blocking.

        This is exactly equivalent to `put(item)` and is only provided
        for compatibility with the Queue class.
        """
        pass

    def qsize(self):  # real signature unknown
        """ Return the approximate size of the queue (not reliable!). """
        pass

    @staticmethod  # known case of __new__
    def __new__(*args, **kwargs):  # real signature unknown
        """ Create and return a new object.  See help(type) for accurate signature. """
        pass
