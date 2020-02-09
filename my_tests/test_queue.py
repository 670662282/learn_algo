import unittest

from my_queue import MyQueue


class TestQueueCase(unittest.TestCase):

    def test_empty(self):
        queue = MyQueue(4)
        self.assertTrue(queue.empty())
        queue.append(2)
        queue.pop_left()
        self.assertTrue(queue.empty())

    def test_full(self):
        queue = MyQueue(3)
        self.assertFalse(queue._full())
        queue.append(1)
        queue.append(2)
        queue.append(3)
        self.assertTrue(queue._full())

    def test_queue_1(self):
        queue = MyQueue(3)
        queue.pop_left()

    def test_queue_2(self):
        queue = MyQueue(3)
        queue.append(0)
        queue.append(1)
        queue.append(2)
        queue.append(3)

    def test_queue_3(self):
        queue = MyQueue(5)
        queue.append(1)
        queue.append(2)
        self.assertEqual(1, queue.pop_left())


if __name__ == '__main__':
    unittest.main()
