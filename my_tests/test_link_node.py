import unittest

from linked import create_bi_directional_link_list, MyLinkNode


class LinkNodeTestCase(unittest.TestCase):

    def test_create_bi_link(self):
        node = create_bi_directional_link_list([1, 2, 3, 4])
        current = node.next
        result = []
        while current.value is not None:
            result.append(current.value)
            current = current.next
        self.assertListEqual(result, [1, 2, 3, 4])

    def test_my_link_node(self):
        link_node = MyLinkNode(1)
        result = []
        for i in link_node:
            result.append(i)
        self.assertListEqual(result, [1])

    def test_my_link_node_2(self):
        link_node = MyLinkNode()
        link_node.append(5)
        self.assertFalse(link_node.is_empty())
        self.assertEqual('5', str(link_node))
        self.assertEqual(len(link_node), 1)

    def test_my_link_node_3(self):
        link_node = MyLinkNode()
        link_node.append(5)
        link_node.append(5)
        self.assertEqual(len(link_node), 2)
        self.assertEqual(str(link_node), '5 5')

    def test_my_link_node_4(self):
        link_node = MyLinkNode(1)
        link_node.append(5)
        link_node.append(4)
        self.assertEqual(len(link_node), 3)
        self.assertEqual(str(link_node), '1 5 4')

    def test_my_link_node_5(self):
        link_node = MyLinkNode()
        self.assertTrue(link_node.is_empty())

    def test_my_link_node_6(self):
        link_node = MyLinkNode()
        link_node.append(3)
        self.assertFalse(link_node.is_empty())

        link_node.insert(value=4)
        self.assertFalse(link_node.is_empty())
        self.assertEqual('4 3', str(link_node))

    def test_my_link_node_7(self):
        link_node = MyLinkNode()
        with self.assertRaises(ValueError):
            link_node.remove(3)

    def test_my_link_node_8(self):
        link_node = MyLinkNode(3, 4)
        link_node.remove(3)
        self.assertFalse(link_node.is_empty())
        self.assertEqual(len(link_node), 1)

        link_node.remove(4)
        self.assertTrue(link_node.is_empty())
        self.assertEqual(len(link_node), 0)

    def test_my_link_node_9(self):
        link_node = MyLinkNode(3, 5)
        value = link_node.pop()
        self.assertEqual(value, 5)
        self.assertFalse(link_node.is_empty())
        self.assertEqual(len(link_node), 1)

        value = link_node.pop()
        self.assertEqual(value, 3)
        self.assertTrue(link_node.is_empty())
        self.assertEqual(len(link_node), 0)

    def test_my_link_node_10(self):
        link_node = MyLinkNode(1)
        link_node.insert(value=6)
        link_node.insert(value=7)
        self.assertEqual('7 6 1', str(link_node))
        link_node.append(3)
        self.assertEqual('7 6 1 3', str(link_node))

    def test_my_link_node_11(self):
        link_node = MyLinkNode()
        link_node.insert(value=6)
        link_node.insert(value=7)
        self.assertEqual('7 6', str(link_node))
        link_node.append(3)
        self.assertEqual('7 6 3', str(link_node))

    def test_my_link_node_12(self):
        link_node = MyLinkNode()
        link_node.append(6)
        link_node.append(7)
        self.assertEqual('6 7', str(link_node))
        link_node.insert(value=3)
        self.assertEqual('3 6 7', str(link_node))

    def test_my_link_node_13(self):
        link_node = MyLinkNode()
        link_node.extend([2, 0, 7])
        link_node.extend([4, 59, 22])
        print(link_node)
        self.assertEqual(str(link_node), '2 0 7 4 59 22')

    def test_my_link_clear(self):
        link_node = MyLinkNode(2, 2, 1)
        link_node.clear()
        link_node.append(3)
        self.assertEqual(str(link_node), '3')

    def test_insert(self):
        link_node = MyLinkNode(1, 2, 3, 4, 5, 6)
        link_node.insert(6, 11)
        self.assertEqual('1 2 3 4 5 6 11', str(link_node))

    def test_insert_2(self):
        link_node = MyLinkNode(1, 2, 3, 4, 5, 6)
        link_node.insert(5, 11)
        self.assertEqual('1 2 3 4 5 11 6', str(link_node))

    def test_pop_1(self):
        link_node = MyLinkNode(1, 2, 3, 4, 5, 6)
        self.assertEqual(1, link_node.pop(0))
        self.assertEqual('2 3 4 5 6', str(link_node))

    def test_pop_2(self):
        link_node = MyLinkNode(1, 2, 3, 4, 5, 6)
        self.assertEqual(6, link_node.pop(5))
        self.assertEqual('1 2 3 4 5', str(link_node))

    def test_pop_3(self):
        link_node = MyLinkNode(1, 2, 3, 4, 5, 6)

        with self.assertRaises(IndexError):
            link_node.pop(6)

    def test_pop_4(self):
        link_node = MyLinkNode(1, 2, 3, 4, 5, 6)
        link_node.pop()
        link_node.pop()
        link_node.pop()
        link_node.pop()
        link_node.pop()
        link_node.pop()
        with self.assertRaises(IndexError):
            link_node.pop()

    def test_link_get(self):
        link_node = MyLinkNode(1, 2, 3, 4, 5, 6)
        self.assertEqual(link_node[0], 1)
        self.assertEqual(link_node[5], 6)

        with self.assertRaises(IndexError):
            x = link_node[6]

    def test_link_get_2(self):
        link_node = MyLinkNode(1, 2, 3, 4, 5, 6)
        self.assertEqual(link_node[-1], 6)
        self.assertEqual(link_node[-2], 5)
        self.assertEqual(link_node[-3], 4)

        with self.assertRaises(IndexError):
            x = link_node[-7]


if __name__ == '__main__':
    unittest.main()
