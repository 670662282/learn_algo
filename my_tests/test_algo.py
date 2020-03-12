import unittest

from algo.back_tracking import queens_8, backpack


class TestBacktrackingALGO(unittest.TestCase):
    def test_queens_8(self):
        times = {
            'times': 0
        }
        queens_8(0, times)
        self.assertEqual(times['times'], 92)

    def test_backpack(self):
        a = [8, 4, 15, 20, 88, 12, 65, 33, 98, 19]
        # 假设背包可承受重量100，物品个数10，物品重量存储在数组a中，那可以这样调用函数
        max_weight = backpack(a, 360)
        self.assertEqual(max_weight['max_weight'], 358)

    def test_re_match(self):
        """正则
        """


if __name__ == '__main__':
    unittest.main()
