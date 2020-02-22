
class Node:
    def __init__(self, value=None):
        self.value = value
        self.next = None


class BiDirectionalNode(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.previous = None


class MyLinkNode:
    """双向循环链表实现list数据结构
    """
    def __init__(self, *args):
        self.head = create_bi_directional_link_list(args)

    @property
    def first_node(self):
        return self.head.next

    @property
    def last_node(self):
        return self.head.previous

    def __str__(self):
        return ' '.join(str(item) for item in self)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.__str__())

    def __contains__(self, item):
        pass

    def __delitem__(self, key):
        pass

    def __setitem__(self, key, value):
        pass

    def __getitem__(self, item):
        if isinstance(item, slice):
            raise ValueError("暂时不支持分片")

        if isinstance(item, int):
            if item >= 0:
                i = 0
                current = self.first_node
                while current != self.head:
                    if i == item:
                        break
                    i += 1
                    current = current.next
                else:
                    raise IndexError('list index out of range')
            else:
                i = -1
                current = self.last_node
                while current != self.head:
                    if i == item:
                        break
                    i -= 1
                    current = current.previous
                else:
                    raise IndexError('list index out of range')

            return current.value

    def __iter__(self):
        self._cur = self.first_node
        return self

    def __next__(self):
        if self._cur == self.head:
            print(f' cur value :{self._cur.value}')
            print(f' cur next value :{self._cur.next.value}')
            print(f' cur next next value :{self._cur.next.next.value}')
            print(f' cur next next next value :{self._cur.next.next.next.value}')
            print(f' cur next next next next value :{self._cur.next.next.next.next.value}')

            print(f' cur previous value :{self._cur.previous.value}')
            print(f' cur previous previous value :{self._cur.previous.previous.value}')
            print(f' cur previous previous previous value :{self._cur.previous.previous.previous.value}')
            print(f' cur previous previous previous previous value :{self._cur.previous.previous.previous.previous.value}')

            raise StopIteration

        value = self._cur.value
        self._cur = self._cur.next
        return value

    def __len__(self):
        return self.count()

    def recursive_reverse(self):
        pass

    def reverse(self):
        """反转链表
        """
        prev = self.head
        current = self.head

        while current.next != self.head:
            print(f'prev.value: {prev.value}')
            current.next, current.previous = prev, current.next
            prev = current  # 更新prev，向后移动
            print(f'after prev.value: {prev.value}')
            current = current.previous  # 更新current，向后移动

        # 到达链表尾部时，需要特殊处理
        current.next = prev
        current.previous = self.head
        self.head.next = current

    def reverse_3(self):
        # todo 有问题
        prev = self.head
        current = self.head  # 将头节点保存在current中

        # 当链表为非空的时候，需要执行相应反转的操作
        # 分别将相邻的两个节点的前驱后继关系进行反转
        while current.next != self.head:
            # next_node = current.next  # 将下一个节点保存在next_node中
            # current.next = prev  # 由于反转链表，因此头节点反转后，成为尾节点，应该指向self.head
            # current.previous = next_node  # 尾节点的前驱应指向原本的后继
            print(f'prev.value: {prev.value}')
            current.next, current.previous = prev, current.next

            prev = current  # 更新prev，向后移动

            print(f'after prev.value: {prev.value}')
            # current = next_node  # 更新current，向后移动
            current = current.previous

        # 到达链表尾部时，需要特殊处理
        # print(current.value)  == 3
        current.next = prev
        current.previous = self.head
        self.head.next = current

    def sort(self):
        pass

    def extend(self, other_list: list):
        head = create_bi_directional_link_list(other_list)
        first_node = head.next
        last_node = head.previous

        self.last_node.next = first_node
        first_node.previous = self.last_node

        last_node.next = self.head
        self.head.previous = last_node

    def clear(self):
        self.head.next = self.head
        self.head.previous = self.head

    def count(self):
        i = 0
        current = self.first_node
        while current != self.head:
            current = current.next
            i += 1
        return i

    def is_empty(self):
        return self.last_node == self.first_node == self.head

    def insert(self, index=0, value=None):
        new_node = BiDirectionalNode(value)

        i = 0
        current = self.first_node
        while current != self.head:
            if i == index:
                pre = current.previous
                pre.next = new_node

                new_node.previous = pre
                new_node.next = current

                current.previous = new_node
                break
            i += 1
            current = current.next
        else:
            # 处理尾节点
            pre = self.head.previous
            pre.next = new_node
            new_node.previous = pre
            new_node.next = self.head
            self.head.previous = new_node

    def append(self, value):
        """插入value到最后一位"""
        last_node = self.last_node
        new_node = BiDirectionalNode(value)

        self.head.previous = new_node

        new_node.next = self.head
        new_node.previous = last_node

        last_node.next = new_node

    def remove(self, value):
        if self.is_empty():
            raise ValueError('LinkNode item is None')
        current = self.first_node

        while current != self.head:
            if current.value == value:
                print('find it')
                return self._delete_node(current)
            current = current.next
        else:
            raise ValueError(f'{value} not in LinkNode')

    def _delete_node(self, current):
        value = current.value
        current.previous.next = current.next
        current.next.previous = current.previous
        current.next = None
        current.previous = None
        return value

    def pop(self, index: int = None):
        if self.is_empty():
            raise IndexError('pop from empty list')

        if index is None:
            value = self.last_node.value
            last_node = self.last_node

            last_node.previous.next = self.head
            self.head.previous = last_node.previous
            return value
        else:
            i = 0
            current = self.first_node
            while current != self.head:
                if i == index:
                    self._delete_node(current)
                    return current.value
                i += 1
                current = current.next

            raise IndexError('pop index out of range')


def create_link_list(link_list):
    """创建一个循环单链表"""
    head = Node()
    pre = head
    for value in link_list:
        new_node = Node(value)
        pre.next = new_node
        pre = new_node

    pre.next = head
    return head


def create_bi_directional_link_list(link_list):
    """创建一个双向循环单链表"""
    head = BiDirectionalNode()
    pre = head
    for value in link_list:
        new_node = BiDirectionalNode(value)

        pre.next = new_node
        new_node.previous = pre

        pre = new_node

    pre.next = head
    head.previous = pre
    return head


if __name__ == '__main__':
    link_node = MyLinkNode(1, 2, 3, 4, 5, 6)
    # print(link_node[0])
    # print(link_node[5])
    print(link_node[-1])
    print(link_node[-2])
    print(link_node[-3])

    x = [1, 2]

    x[6] = 2
    del x[0]

    print(x)

   # x.insert(6, 11)

