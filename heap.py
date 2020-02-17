class Heap:
    """大堆 基于数组实现
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

    def insert(self, value):
        if self.count > len(self.items):
            return
        self.count += 1
        self.items[self.count] = value
        current = self.count
        # 自下往上堆化
        while current // 2 >= self.__top_pos and self.items[current] > self.items[current//2]:
            # 交换
            self.__swap(current // 2, current)
            current = current // 2

    def remove_max_value(self):
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
            for index in range(len(result)-1, -1, -1):
                result[index] = self.remove_max_value()
        else:
            for index in range(len(result)):
                result[index] = self.remove_max_value()

        self.items = item_bak
        self.count = count_bak
        return result







