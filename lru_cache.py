from weakref import proxy
from functools import lru_cache


class _Link:
    """ link node,  use __weakref__ to prevent circular references
     __slots__ allow us to explicitly declare data members
     (like properties) and deny the creation of __dict__ and __weakref__ 
     (unless explicitly declared in __slots__ or available in a parent.)

     Without a __weakref__ variable for each instance, classes defining __slots__ do not support weak references to its instances.
     If weak reference support is needed, then add '__weakref__' to the sequence of strings in the __slots__ declaration.
    """
    __slots__ = 'prev', 'next', 'key', 'value', '__weakref__'


class LRUCache:
    """LRU cache based on hash table and doubly circular linked list
    The internal self.__map dict maps keys to links in a doubly linked list.

    The circular doubly linked list starts and ends with a sentinel element.

    The sentinel element never gets deleted (this simplifies the algorithm).

    The sentinel is in self.__hardroot with a weakref proxy in self.__root.

    The prev links are weakref proxies (to prevent circular references).

    Individual links are kept alive by the hard reference in self.__map.
    """
    def __init__(self, capacity=512):
        self._capacity = capacity
        self.__hard_root = _Link()
        self.__root = proxy(self.__hard_root)
        # init doubly circular linked list
        self.__root.prev = self.__root.next = self.__root
        self.__map = {}

    def get(self, key):
        result = self.__map.get(key)
        if result:
            self._move_to_end(key)
        return result

    def clear(self):
        """Clear the cache."""
        self.__map.clear()
        self.__root.prev = self.__root.next = self.__root

    def __len__(self):
        """Return the current size of the cache."""
        return len(self.__map)

    def __iter__(self):
        root = self.__root
        current = root.prev
        while current is not root:
            yield current.key, current.value
            current = current.prev

    def __repr__(self):
        return f'[{self.__class__.__name__}]({self.__map})'

    def _move_to_end(self, key):
        node = self.__map[key]
        root = self.__root

        # 从链表中断开node
        node.prev.next = node.next
        node.next.prev = node.prev

        # 添加到尾节点
        prev = root.prev
        prev.next = node
        node.prev = prev
        node.next = root
        root.prev = node

    def delete(self, key):
        node = self.__map.pop(key, None)
        if node:
            node.prev.next = node.next
            node.next.prev = node.prev
            node.prev = None
            node.next = None

    def set(self, key, value):
        root = self.__root

        result = self.__map.get(key)
        if result:
            # 移动到尾节点 并更新
            self._move_to_end(key)
            if result.value != value:
                root.prev.value = value

        else:
            # 是否满了
            if len(self.__map) >= self._capacity:
                # 删除头结点
                root = self.__root
                first_node = root.next
                root.next = first_node.next
                first_node.next.prev = root

            # 添加到尾结点
            node = _Link()
            node.key, = key
            node.value = value

            prev = root.prev
            prev.next = node
            node.prev = prev
            node.next = root
            # head头结点 都是引用 弱引用对象
            root.prev = proxy(node)
            self.__map[key] = node


if __name__ == '__main__':
    """
       hashtable 是无序的，无法实现LRU缓存系统， 缓存满了，没办法删除最早使用的数据，
       为什么不直接用双向链表实现LRU缓存系统， 因为LRU主要的增删查都需要查找数据。
       查找数据需要遍历链表，所以单纯用链表实现的 LRU 缓存淘汰算法的时间复杂很高，是 O(n)。
       我们需要维护一个按照访问时间从大到小有序排列的链表结构。
       因为缓存大小有限，当缓存空间不够，需要淘汰一个数据的时候，我们就直接将链表头部的结点删除。
       当要缓存某个数据的时候，先在链表中查找这个数据。如果没有找到，则直接将数据放到链表的尾部；
       如果找到了，我们就把它移动到链表的尾部。因为查找数据需要遍历链表，所以单纯用链表实现的 LRU 缓存淘汰算法的时间复杂很高，是 O(n)。

       了解了这个散列表和双向链表的组合存储结构之后，我们再来看，前面讲到的缓存的三个操作，是如何做到时间复杂度是 O(1) 的？
       首先，我们来看如何查找一个数据。我们前面讲过，散列表中查找数据的时间复杂度接近 O(1)，

       所以通过散列表，我们可以很快地在缓存中找到一个数据。当找到数据之后，我们还需要将它移动到双向链表的尾部。

       其次，我们来看如何删除一个数据。我们需要找到数据所在的结点，然后将结点删除。借助散列表，
       我们可以在 O(1) 时间复杂度里找到要删除的结点。


       因为我们的链表是双向链表，双向链表可以通过前驱指针 O(1) 时间复杂度获取前驱结点，
       所以在双向链表中，删除结点只需要 O(1) 的时间复杂度。


       最后，我们来看如何添加一个数据。添加数据到缓存稍微有点麻烦，我们需要先看这个数据是否已经在缓存中。
       如果已经在其中，需要将其移动到双向链表的尾部；如果不在其中，还要看缓存有没有满。


       如果满了，则将双向链表头部的结点删除，然后再将数据放到链表的尾部；如果没有满，就直接将数据放到链表的尾部。
       这整个过程涉及的查找操作都可以通过散列表来完成。


       其他的操作，比如删除头结点、链表尾部插入数据等，都可以在 O(1) 的时间复杂度内完成。
       所以，这三个操作的时间复杂度都是 O(1)。
       至此，我们就通过散列表和双向链表的组合使用，实现了一个高效的、支持 LRU 缓存淘汰算法的缓存系统原型。

       """
    cache = LRUCache()
    cache.set('a', 1)
    cache.set('b', 2)
    cache.set('c', 3)
    cache.set('d', 4)

    cache.set('a', 'a')
    x = cache.get('c')
    list_ = []
    for k, v in cache:
        list_.append(f'{k}{v}')

    assert list_ == ['c3', 'aa', 'd4', 'b2']
