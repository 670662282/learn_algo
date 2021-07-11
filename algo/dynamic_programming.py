
"""
“杨辉三角”不知道你听说过吗？我们现在对它进行一些改造。
每个位置的数字可以随意填写，经过某个数字只能到达下面一层相邻的两个数字。
假设你站在第一层，往下移动，我们把移动到最底层所经过的所有数字之和，定义为路径的长度。
请你编程求出从最高层移动到最底层的最短路径长度
"""

import random


def init_(level: int):

    items = []
    for i in range(1, level+1):
        items.extend([
            [random.randint(1, 99) for _ in range(i)]
        ])
    return items


init_list = init_(5)  # e.x: [[7], [46, 56], [15, 76, 99], [64, 72, 50, 42], [2, 76, 60, 23, 62]]


def start_1(items):
    """状态转移 从上到下
    :param items:
    :return:
    """
    deep_len = len(items)
    states = [[0] * i for i in range(1, deep_len+1)]
    states[0][0] = items[0][0]
    for i in range(1, deep_len):
        for j in range(len(items[i])):
            if j == 0:
                states[i][j] = states[i-1][j] + items[i][j]
            elif j == len(items[i]) - 1:
                states[i][j] = states[i-1][j-1] + items[i][j]
            else:
                states[i][j] = min(states[i-1][j], states[i-1][j-1]) + items[i][j]

    return min(states[-1])


def start_2(items):
    """方程转移 从下到上
    :param items:
    :return:
    """
    deep_len = len(items)
    # 为了解决边界问题，数组容量多+1
    states = [0] * (deep_len+1)
    print("start_2:")
    for i in reversed(range(deep_len)):

        for j in range(len(items[i])):
            # 左父节点 和右父节点的最小值
            # min({states[j]}, {states[j+1]}) 找到 上一个状态的左值和 上一个状态的右值（就是），中的最小值
            print(f'states[{j}] = min({states[j]}, {states[j+1]})+ {items[i][j]}')
            states[j] = min(states[j], states[j+1]) + items[i][j]
        print(f'{states=}')
    return states[0]


if __name__ == '__main__':
    print(f"init_list: {init_list}")
    #init_list = [[5], [7, 8], [2, 3, 4], [4, 9, 6, 1], [2, 7, 9, 4, 5]]
    print(f'{start_1(init_list)=}')
    print()
    print(f'{start_2(init_list)=}')
