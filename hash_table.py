import logging

logging.basicConfig(level=logging.DEBUG
                    , format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


class _ListNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


def hash_table_to_dict(table):
    table = table or []
    result = {}
    for node in table:
        if node is not None:
            while node is not None:
                result[node.key] = node.value
                node = node.next

    return result


def get_hash_table(table):
    table = table or []

    result = []
    for i, node in enumerate(table):
        node_dict = {}
        while node is not None:
            node_dict[node.key] = node.value
            node = node.next
        result.append(node_dict)

    return result


class HashMap:
    """
    无序字典
    单向链表解决散列冲突
    todo 红黑树代替单向链表
    """

    def __init__(self, table_size=16):
        self._table_size = table_size
        self._table = [None] * self._table_size
        self._new_table = None  # 扩容之后 数据分次搬移到 new_table
        self._size = 0  # number of nodes in the map
        self._LOAD_FACTOR = 0.75

    def __len__(self):
        return self._size

    def __str__(self):
        return f'{self.to_dict()}'

    def __contains__(self, key):
        """ True if the dictionary has the specified key, else False. """
        return False if self._find_node_in_table(key)[0] is None else True

    def to_dict(self):
        result = {}
        result.update(hash_table_to_dict(self._new_table))
        result.update(hash_table_to_dict(self._table))

        return result

    def print_self(self):
        return f'table: {get_hash_table(self._table)} \n new_table: {get_hash_table(self._new_table)}'

    def _hash(self, key):
        return abs(hash(key)) % len(self._table)

    def _new_hash(self, key):
        return abs(hash(key)) % len(self._new_table)

    def __iter__(self):
        pass

    def __getitem__(self, key):

        node = self._find_node_in_table(key)[0]
        if node is None:
            raise KeyError(f'{key}')
        return node.value

    def __setitem__(self, key, value):
        self.insert(key, value)

    def __delitem__(self, key):
        self.pop(key)

    def copy(self):
        """od.copy() -> a shallow copy of od"""
        return self.__class__(self)

    def clear(self):
        """ D.clear() -> None.  Remove all items from D. """
        self._table = [None] * self._table_size
        self._new_table = None
        self._size = 0

    def items(self):
        """ D.items() -> a set-like object providing a view on D's items """
        pass

    def values(self):
        """ D.values() -> an object providing a view on D's values """
        pass

    def keys(self):
        """ D.keys() -> a set-like object providing a view on D's keys """
        pass

    @classmethod
    def fromkeys(cls, iterable, value=None):
        """Create a new dictionary with keys from iterable and values set to value.
        """
        self = cls()
        for key in iterable:
            self[key] = value
        return self

    __marker = object()

    def pop(self, key, default=__marker):
        """
        D.pop(k[,d]) -> v, remove specified key and return the corresponding value.
        If key is not found, d is returned if given, otherwise KeyError is raised
        """
        node, table, index = self._find_node_in_table(key)
        if node is None:
            if default is self.__marker:
                raise KeyError(f'{key}')
            else:
                return default

        # 没有散列冲突
        if node.key == key:
            table[index] = node.next
            self._size -= 1
            return node.value
        else:
            # 散列冲突后 冲突的值放入单向链表
            while node.next is not None:
                pre = node
                node = node.next
                if node.key == key:
                    pre.next = node.next
                    self._size -= 1
                    return node.vaule

    def popitem(self):
        """
        D.popitem() -> (k, v), remove and return some (key, value) pair as a
        2-tuple; but raise KeyError if D is empty.
        """
        pass

    def setdefault(self, key, default=None):
        """Insert key with a value of default if key is not in the dictionary.
        Return the value for key if key is in the dictionary, else default.
        """
        if key in self:
            return self[key]
        self[key] = default
        return default

    def update(self, other_dict: dict):
        """
        """
        if not isinstance(other_dict, dict):
            raise TypeError(f'other_dict must dictionary type')
        for key, value in other_dict.items():
            self.insert(key, value)

    def get(self, key, default=None):
        node = self._find_node_in_table(key)[0]
        if node is None:
            return default
        return node.value

    def resize(self):
        """只申请新空间，但并不将旧的数据立即搬移到新散列表中，而是分批次搬移，每次操作只搬移一个数据
        避免扩容的时候影响性能， 搬移操作时间均摊每次插入中
        :return:
        """

        if self._new_table is not None:
            logger.debug('self._table = self._new_table')
            self._table = self._new_table

        self._new_table = [None] * len(self._table) * 2
        self.__move_one_data()

    def __move_one_data(self):
        logger.debug(
            f'before table: {get_hash_table(self._table)}')
        logger.debug(f'before new_table: {get_hash_table(self._new_table)}')

        if self._new_table is not None:
            for i, node in enumerate(self._table):
                if node is not None:
                    index = self._new_hash(node.key)
                    logger.debug(f'搬移数据: {node.key}, new_hash_index: {index}')

                    # 搬移一位
                    old_node = self._new_table[index]
                    next_node = node.next
                    node.next = old_node

                    self._new_table[index] = node
                    self._table[i] = next_node
                    break
                continue
            else:
                logger.debug('old table 已经搬空')
                self._table = self._new_table
                self._new_table = None

        logger.debug(f'after table: {get_hash_table(self._table)}')
        logger.debug(f'after new_table: {get_hash_table(self._new_table)}')
        logger.debug('')

    def insert(self, key, value):
        """ insert key value in dictionary. only update value if dictionary has the specified key
        :param key:
        :param value:
        :return:
        """
        node = self._find_node_in_table(key)[0]
        if node is None:
            if self._size >= self._table_len() * self._LOAD_FACTOR:
                logger.debug('start resize')
                self.resize()

            self.__insert_value(key, value)
        else:
            if node.value != value:
                logger.debug('存在相同key，只更新value')
                node.value = value

    def _table_len(self):
        return len(self._table) if self._new_table is None else len(self._new_table)

    def __insert_value(self, key, value):
        logger.debug(f'insert new key. key: {key}, value: {value}')

        if self._new_table is not None:
            index = self._new_hash(key)
            old_node = self._new_table[index]
            self._new_table[index] = _ListNode(key, value)
            self._new_table[index].next = old_node
            self.__move_one_data()
        else:
            index = self._hash(key)
            old_node = self._table[index]
            self._table[index] = _ListNode(key, value)
            self._table[index].next = old_node

        self._size += 1

    def _get_node(self, node, key):
        while node is not None:
            if node.key == key:
                return node
            else:
                logger.debug(f'pass -> {node.key}')
            node = node.next

    def _find_node_in_new_table(self, key):
        if self._new_table is None:
            return None, None
        hash_index = self._new_hash(key)
        node = self._new_table[hash_index]
        return self._get_node(node, key), hash_index

    def _find_node_in_old_table(self, key):
        hash_index = self._hash(key)
        node = self._table[hash_index]
        return self._get_node(node, key), hash_index

    def _find_node_in_table(self, key):
        """
        :param key:
        :return: node and table and hash_index
        """
        node, hash_index = self._find_node_in_new_table(key)

        if node is None:
            node, index = self._find_node_in_old_table(key)
            if node is None:
                table = None
                hash_index = None
            else:
                table = self._table
                hash_index = index
        else:
            table = self._new_table

        return node, table, hash_index


if __name__ == '__main__':
    map = HashMap(3)
    map.insert('a', '1')
    map.insert('a', 'a')
    map.insert('b', '2')
    map.insert('c', '3')
    map.insert('d', '4')
    map.insert('e', '5')
    map.insert('f', '6')
    print(map)

    print('map["a"]:' + map['a'])
    print('map["b"]:' + map['b'])
    print('map["c"]:' + map['c'])
    print('map["d"]:' + map['d'])
    print('map["e"]:' + map['e'])
    print('map["f"]:' + map['f'])

    print(map.setdefault('a', '123'))
    print(map.setdefault('aa', '123'))

    x = {'d': 2, 'a': '1', 'b': '2', 'c': 3}
    print(x.pop('z', 2))
    print(x.items())
    x.setdefault('ad', 3)


