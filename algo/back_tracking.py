"""
回溯算法应用

八皇后、0-1 背包问题、图的着色、旅行商问题、数独、全排列、正则表达式匹配
"""

"""
八皇后

我们有一个 8x8 的棋盘，希望往里放 8 个棋子（皇后），每个棋子所在的行、列、对角线都不能有另一个棋子。
八皇后问题就是期望找到所有满足这种要求的放棋子方式。

我们把这个问题划分成 8 个阶段，依次将 8 个棋子放到第一行、第二行、第三行……第八行。
在放置的过程中，我们不停地检查当前放法，是否满足要求。
如果满足，则跳到下一行继续放置棋子；如果不满足，那就再换一种放法，继续尝试。
"""
result = [-1] * 8  # 下标表示行,值表示queen存储在哪一列


def queens_8(row: int, times):
    """
    回溯是怎么执行的

    简单来说，当前几个循环皇后按照要求站好位之后，已经产生了对应数量的递归栈，
    此时一致是递归中的递，当走到当前循环时检查发现 某个检查isOK都是false时，这个时候就该递归中的归了，所以就回到上一行，
    为该行的皇后换另外一个符合条件的位置，再次递归，直到遍历所有可能的结果 这就是所谓的枚举搜索
    """
    if row == 8:
        print(result)
        print_queens(times)
        return

    for column in range(8):
        if is_ok(row, column):
            result[row] = column  # 第row行的棋子放到了column列
            queens_8(row + 1, times)  # 检查下一行


def is_ok(row, column):
    """判断row行column列放置是否合适
    """
    left_up = column - 1  # 左上对角线
    right_up = column + 1  # 右上对角线

    for i in reversed(range(row)):  # 逐行往上考察每一行
        if result[i] == column:  # 检查第i行的column列有棋子
            return False

        if 0 <= left_up == result[i]:  # 检查第i行left_up列有棋子吗
            return False

        if 0 <= right_up == result[i]:  # 检查第i行right_up列有棋子吗
            return False

        left_up -= 1
        right_up += 1

    return True


def print_queens(times):
    """打印出一个二维矩阵
    """
    times['times'] += 1
    for row in range(len(result)):
        for column in range(len(result)):
            if result[row] == column:
                print('Q ', end=' ')
            else:
                print('* ', end=' ')
        print()
    print()


"""
0-1 背包问题
0-1 背包是非常经典的算法问题，很多场景都可以抽象成这个问题模型
0-1 背包问题有很多变体

我们有一个背包，背包总的承载重量是 Wkg。
现在我们有 n 个物品，每个物品的重量不等，并且不可分割。
我们现在期望选择几件物品，装载到背包中。在不超过背包所能装载重量的前提下，如何让背包中物品的总重量最大？
物品是不可分割的，要么装要么不装，所以叫 0-1 背包问题

对于每个物品来说，都有两种选择，装进背包或者不装进背包。
对于 n 个物品来说，我们可以把物品依次排列，整个问题就分解为了 n 个阶段，
每个阶段对应一个物品怎么选择。先对第一个物品进行处理，选择装进去或者不装进去，
然后再递归地处理剩下的物品。
这里还稍微用到了一点搜索剪枝的技巧，就是当发现已经选择的物品的重量超过 Wkg 之后，我们就停止继续探测剩下的物品。
"""


def backpack(list_a: list, backpack_weight):
    max_weight = dict(max_weight=0)  # 背包中物品总重量的最大值
    input_in_backpack(0, 0, list_a, len(list_a), backpack_weight, max_weight)
    return max_weight


def input_in_backpack(i, current_weight, items, nums, backpack_max_weight, result):
    # 如果装满了或者 考察所有物品
    if current_weight == backpack_max_weight or i == nums:
        if current_weight > result['max_weight']:
            result['max_weight'] = current_weight
        return
    # 当前物品不装进背包  穷举每种可能的情况
    input_in_backpack(i + 1, current_weight, items, nums, backpack_max_weight, result)

    # 没有超过背包承受的重量的时候，当前物品装进背包
    if current_weight + items[i] <= backpack_max_weight:
        input_in_backpack(i + 1, current_weight + items[i], items, nums, backpack_max_weight, result)


"""
正则表达式
正则表达式中，最重要的就是通配符，通配符结合在一起，可以表达非常丰富的语义。
为了方便讲解，我假设正则表达式中只包含“*”和“?”这两种通配符，
并且对这两个通配符的语义稍微做些改变，其中，“*”匹配任意多个（大于等于 0 个）任意字符，“?”匹配零个或者一个任意字符。
基于以上背景假设，我们看下，如何用回溯算法，判断一个给定的文本，能否跟给定的正则表达式匹配？


我们依次考察正则表达式中的每个字符，当是非通配符时，我们就直接跟文本的字符进行匹配，如果相同，则继续往下处理；如果不同，则回溯。
如果遇到特殊字符的时候，我们就有多种处理方式了，也就是所谓的岔路口，
比如“*”有多种匹配方案，可以匹配任意个文本串中的字符，我们就先随意的选择一种匹配方案，然后继续考察剩下的字符。
如果中途发现无法继续匹配下去了，我们就回到这个岔路口，重新选择一种匹配方案，然后再继续匹配剩下的字符。
"""


class Pattern:
    def __init__(self, pattern):
        self.pattern_ = pattern
        self.matchd = False

    def match(self, str_content):
        self.rmatch(0, 0, str_content)

    def rmatch(self, text_pos, pattern_pos, str_text):

        if self.matchd is True:
            return

        if pattern_pos == len(str_text):
            if text_pos == len(self.pattern_):
                self.matchd = True
            return

        # 匹配任意字符
        if self.pattern_[pattern_pos] == '*':
            for k in range(len(str_text) - text_pos):
                self.rmatch(text_pos + k, pattern_pos + 1, str_text)

        elif self.pattern_[pattern_pos] == '?':
            self.rmatch(text_pos, pattern_pos + 1, str_text)
            self.rmatch(text_pos + 1, pattern_pos + 1, str_text)

        elif text_pos < len(str_text) and self.pattern_[pattern_pos] == str_text[text_pos]:
            self.rmatch(text_pos + 1, pattern_pos + 1, str_text)
