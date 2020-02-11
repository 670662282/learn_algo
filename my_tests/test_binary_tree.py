import unittest

from binary_tree import BinarySearchTree, in_order


class TestBinarySearchTree(unittest.TestCase):
    def test_tree(self):
        tree = BinarySearchTree()
        tree.insert(3)
        tree.insert(4)
        tree.insert(1)
        tree.insert(8)
        tree.insert(4)
        self.assertEqual([1, 3, 4, 4, 8], tree.to_list())

    def test_tree_2(self):
        tree = BinarySearchTree()
        tree.insert(3)
        tree.insert(4)
        tree.insert(1)
        tree.insert(8)
        tree.insert(8)
        self.assertEqual(8, tree.find_max_value())
        self.assertEqual(1, tree.find_min_value())
        self.assertEqual([1, 3, 4, 8, 8], tree.to_list())

    def test_tree_3(self):
        tree = BinarySearchTree()
        tree.insert(3)
        tree.insert(4)
        tree.insert(1)
        tree.insert(3)
        tree.insert(8)
        tree.insert(8)
        result = tree.find(3)
        self.assertEqual([3, 3], result)

    def test_tree_find(self):
        tree = BinarySearchTree()
        tree.insert(3)
        tree.insert(4)
        tree.insert(1)
        tree.insert(3)
        tree.insert(8)
        tree.insert(8)
        result = []
        for node in tree.find_all(3):
            result.append((node.value, node.parent.value if node.parent else None))
        self.assertEqual([(3, None), (3, 4)], result)

    def test_tree_4(self):
        tree = BinarySearchTree()
        tree.insert(3)
        tree.insert(4)
        tree.insert(1)
        tree.insert(3)
        tree.insert(8)
        tree.insert(8)

        tree.delete(4)
        self.assertEqual([1, 3, 3, 8, 8], tree.to_list())

    def test_tree_5(self):
        tree = BinarySearchTree()
        tree.insert(3)
        tree.insert(4)
        tree.insert(1)
        tree.insert(3)
        tree.insert(8)
        tree.insert(8)

        tree.delete(8)
        self.assertEqual([1, 3, 3, 4], tree.to_list())


if __name__ == '__main__':
    unittest.main()
