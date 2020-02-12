import math
from queue import Queue

from hash_table import logger


class Node:
    def __init__(self, value):
        self.right = self.left = None
        self.value = value
        self.parent = None


class BinarySearchTree:
    """二叉查找树要求，在树中的任意一个节点，
    其左子树中的每个节点的值，都要小于这个节点的值，而右子树节点的值都大于这个节点的值
    """
    def __init__(self):
        self._root = None

    def to_list(self):
        self._result = []
        root = self._root
        self._print(root)
        return self._result

    def _print(self, root):
        if root:
            self._print(root.left)
            self._result.append(root.value)
            self._print(root.right)

    def find(self, value):
        result = []
        for node in self.find_all(value):
            result.append(node.value)
        return result

    def high(self):
        """二叉树的高度, 层级 - 1"""
        root = self._root
        level = 0
        level_queue = [root] if root else []
        while len(level_queue) > 0:
            level += 1
            logger.debug(f'tree: {level} level,  {len(level_queue)} node')

            queue = level_queue[:]
            level_queue = []

            while len(queue) > 0:
                node = queue.pop(0)
                logger.debug(node.value)

                if node.left:
                    level_queue.append(node.left)
                if node.right:
                    level_queue.append(node.right)

            logger.debug('')
        return level - 1

    def find_all(self, value):
        """find 所有值为value的节点列表
        """
        current = self._root

        result = []
        while current:

            if value > current.value:
                current = current.right
            if value < current.value:
                current = current.left

            # 找到目标node，后继续往后查找， 和value相同的只可能出现在树的右边
            if current and value == current.value:
                result.append(current)
                current = current.right

        return result

    def insert(self, value):
        root = self._root
        if root is None:
            self._root = Node(value)
        else:
            self._insert(root, value)

    def _insert(self, root, value):
        if value >= root.value:

            if root.right is None:
                new_node = Node(value)
                new_node.parent = root
                root.right = new_node
            else:
                self._insert(root.right, value)

        if value < root.value:

            if root.left is None:
                new_node = Node(value)
                new_node.parent = root
                root.left = new_node
            else:
                self._insert(root.left, value)

    def delete(self, value):
        """
        第一种情况是，如果要删除的节点没有子节点，我们只需要直接将父节点中，指向要删除节点的指针置为 null。

        第二种情况是，如果要删除的节点只有一个子节点（只有左子节点或者右子节点），
        我们只需要更新父节点中，指向要删除节点的指针，让它指向要删除节点的子节点就可以了。

        第三种情况是，如果要删除的节点有两个子节点，这就比较复杂了。包含前二种情况的处理

        我们需要找到这个节点的右子树中的最小节点，把它替换到要删除的节点上。
        然后再删除掉这个最小节点，因为最小节点肯定没有左子节点（如果有左子结点，那就不是最小节点了）
        删除这个最小节点的时候，可能是第一种情况，也可能是第二种情况
        """
        logger.debug('')
        logger.debug(f'delete_before: {self.to_list()}')

        for node in self.find_all(value):
            logger.debug(f'delete node: {node.value}, last node: {node.parent.value}')

            # 有2个子节点 找到删除节点右子树中最小的值 搬移到这个节点上
            if node.left and node.right:
                logger.debug(
                    '删除节点有2个子节点，不删除这个节点，'
                    '只是将删除节点的值变成该节点右子树中最小的值(最小值节点没有左节点)，'
                    '并删除这个最小的值'
                )
                min_node = self._find_min_node(node.right)
                node.value = min_node.value
                # 删除这个最小节点
                node = min_node

            # 删除节点是叶子节点或者只有一个子节点
            if node.left is not None:
                logger.debug('删除节点只有左节点')
                child = node.left

            elif node.right is not None:
                logger.debug('删除节点只有右节点')
                child = node.right

            else:
                logger.debug('删除节点是叶子节点， 没有子节点')
                child = None

            if child:
                child.parent = node.parent

            # 删除的节点是根节点
            if node.parent is None:
                self._root = child
                self._root.parent = None

            elif node.parent.left == node:
                node.parent.left = child

            else:
                node.parent.right = child

            node.parent = node.left = node.right = None

            logger.debug(f'delete_result: {self.to_list()}')

    def find_min_value(self):
        root = self._root
        return self._find_min_node(root).value

    def find_max_value(self):
        current = self._root
        while current and current.right:
            current = current.right
        return current.value

    def _find_min_node(self, root: Node):
        while root and root.left:
            root = root.left
        return root

    def __repr__(self):
        return self._draw_tree()

    def _bfs(self):
        """
        bfs
        通过父子关系记录节点编号
        :return:
        """
        if self._root is None:
            return []

        ret = []
        q = Queue()
        # 队列[节点，编号]
        q.put((self._root, 1))

        while not q.empty():
            n = q.get()

            if n[0] is not None:
                ret.append((n[0].value, n[1]))
                q.put((n[0].left, n[1] * 2))
                q.put((n[0].right, n[1] * 2 + 1))

        return ret

    def _draw_tree(self):
        """
        可视化
        :return:
        """
        nodes = self._bfs()

        if not nodes:
            print('This tree has no nodes.')
            return

        layer_num = int(math.log(nodes[-1][1], 2)) + 1

        prt_nums = []

        for i in range(layer_num):
            prt_nums.append([None] * 2 ** i)

        for v, p in nodes:
            row = int(math.log(p, 2))
            col = p % 2 ** row
            prt_nums[row][col] = v

        prt_str = ''
        for l in prt_nums:
            prt_str += str(l)[1:-1] + '\n'

        return prt_str


def pre_order(root):
    if root:
        print(root.value)
        pre_order(root.left)
        pre_order(root.right)


def in_order(root):
    if root:
        in_order(root.left)
        print(root.value)
        in_order(root.right)


def post_order(root):
    if root:
        post_order(root.left)
        post_order(root.right)
        print(root.value)


def level_order(root):
    """层次 遍历
    二叉树的层次遍历即从上往下、从左至右依次打印树的节点。
    其思路就是将二叉树的节点加入队列，出队的同时将其非空左右孩子依次入队，出队到队列为空即完成遍历。
    """
    queue = [root]
    while queue != [] and root:
        print(queue[0].value)
        if queue[0].left:
            queue.append(queue[0].left)
        if queue[0].right:
            queue.append(queue[0].right)
        queue.pop(0)


if __name__ == '__main__':
    tree = BinarySearchTree()
    tree.insert(6)
    tree.insert(4)
    tree.insert(8)
    tree.insert(2)
    tree.insert(5)
    tree.insert(7)
    tree.insert(9)
    tree.insert(1)
    tree.insert(3)
    print(tree)
    print(tree.high())
