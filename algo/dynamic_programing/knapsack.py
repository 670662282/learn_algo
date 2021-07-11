"""
 0-1 背包问题

对于一组不同重量、不可分割的物品，我们需要选择一些装入背包，在满足背包最大重量限制的前提下，背包中物品总重量的最大值是多少呢？

我们把整个求解过程分为 n 个阶段，每个阶段会决策一个物品是否放到背包中。
每个物品决策（放入或者不放入背包）完之后，背包中的物品的重量会有多种情况，
也就是说，会达到多种不同的状态，对应到递归树中，就是有很多不同的节点。
我们把每一层重复的状态（节点）合并，只记录不同的状态，然后基于上一层的状态集合，来推导下一层的状态集合。
我们可以通过合并每一层重复的状态，这样就保证每一层不同状态的个数都不会超过 w 个（w 表示背包的承载重量），
也就是例子中的 9。于是，我们就成功避免了每层状态个数的指数级增长。
我们用一个二维数组 states[n][w+1]，来记录每层可以达到的不同状态。

第 0 个（下标从 0 开始编号）物品的重量是 2，要么装入背包，要么不装入背包，决策完之后，会对应背包的两种状态，背包中物品的总重量是 0 或者 2。
我们用 states[0][0]=true 和 states[0][2]=true 来表示这两种状态。

第 1 个物品的重量也是 2，基于之前的背包状态，在这个物品决策完之后，不同的状态有 3 个，背包中物品总重量分别是 0(0+0)，2(0+2 or 2+0)，4(2+2)。
我们用 states[1][0]=true，states[1][2]=true，states[1][4]=true 来表示这三种状态。

以此类推，直到考察完所有的物品后，整个 states 状态数组就都计算好了。我把整个计算的过程画了出来，你可以看看。
图中 0 表示 false，1 表示 true。我们只需要在最后一层，找一个值为 true 的最接近 w（这里是 9）的值，就是背包中物品总重量的最大值。


实际上，这就是一种用动态规划解决问题的思路。
我们把问题分解为多个阶段，每个阶段对应一个决策。我们记录每一个阶段可达的状态集合（去掉重复的），
然后通过当前阶段的状态集合，来推导下一个阶段的状态集合，动态地往前推进。这也是动态规划这个名字的由来
"""


def knapsack(items: list, backpack_max_weight: int):
    """
    weight: 物品重量
    n: 物品个数
    backpack_max_weight: 背包可承载重量
    """
    n = len(items)
    states = [[False] * (backpack_max_weight + 1) for _ in range(n + 1)]

    # 第一行的数据需要特殊处理
    states[0][0] = True
    if items[0] < backpack_max_weight:
        states[0][items[0]] = True

    for i in range(1, n):
        for j in range(backpack_max_weight + 1):  # 不把第i个物品放入背包
            if states[i - 1][j] is True:
                states[i][j] = states[i - 1][j]

        if backpack_max_weight - items[i] < 0:
            continue
        for j in range(backpack_max_weight - items[i] + 1):  # 把第i个物品放入背包
            if states[i - 1][j] is True:
                states[i][j + items[i]] = True

    print(states[n - 1])
    for i in reversed(range(backpack_max_weight+1)):
        if states[n - 1][i] is True:
            return i

    return 0


def knapsack2(items: list, backpack_max_weight: int):
    """一维数组代替二维数组
    """
    n = len(items)
    states = [False] * (backpack_max_weight + 1)

    if items[0] <= backpack_max_weight:
        states[items[0]] = True

    for i in range(1, n):
        if backpack_max_weight - items[i] < 0:
            continue
        for j in reversed(range(backpack_max_weight - items[i] + 1)):  # 倒叙解决for循环重复计算
            if states[j] is True:
                states[j + items[i]] = True

    for i in reversed(range(backpack_max_weight+1)):
        if states[i] is True:
            return i

    return 0


"""
对于一组不同重量、不同价值、不可分割的物品，我们选择将某些物品装入背包，
在满足背包最大重量限制的前提下，背包中可装入物品的总价值最大是多少呢？

我们还是把整个求解过程分为 n 个阶段，每个阶段会决策一个物品是否放到背包中。
每个阶段决策完之后，背包中的物品的总重量以及总价值，会有多种情况，也就是会达到多种不同的状态。
我们用一个二维数组 states[n][w+1]，来记录每层可以达到的不同状态。
不过这里数组存储的值不再是 boolean 类型的了，而是当前状态对应的最大总价值。
我们把每一层中 (i, cw) 重复的状态（节点）合并，只记录 cv 值最大的那个状态，然后基于这些状态来推导下一层的状态。

"""


def knapsack3(items: list, value_list: list, backpack_max_weight: int):
    n = len(items)
    states = [[-1] * (backpack_max_weight + 1) for _ in range(n + 1)]  # states 存储的当前状态对应的最大总价值

    states[0][0] = 0
    if items[0] <= backpack_max_weight:
        states[0][items[0]] = value_list[0]

    for i in range(1, n):
        for j in range(backpack_max_weight + 1):  # 不把第i个物品放入背包
            if states[i - 1][j] >= 0:
                states[i][j] = states[i - 1][j]

        if backpack_max_weight - items[i] < 0:
            continue
        for j in range(backpack_max_weight - items[i] + 1):  # 把第i个物品放入背包
            if states[i - 1][j] >= 0:
                value = states[i - 1][j] + value_list[i]
                if value > states[i][j + items[i]]:  # 记录 cv 值最大的那个状态
                    states[i][j + items[i]] = value
    print(states[n-1])
    return max(states[n-1])


def knapsack4(items: list, value_list: list, backpack_max_weight: int):
    n = len(items)
    states = [-1] * (backpack_max_weight + 1)  # states 存储的当前状态对应的最大总价值

    states[0] = 0
    if items[0] <= backpack_max_weight:
        states[items[0]] = value_list[0]

    for i in range(1, n):
        if backpack_max_weight - items[i] < 0:
            continue
        for j in reversed(range(backpack_max_weight - items[i] + 1)):  # 倒叙解决for循环重复计算
            if states[j] >= 0:
                value = states[j] + value_list[i]
                if value > states[j + items[i]]:
                    states[j + items[i]] = value

    print(states)
    return max(states)


if __name__ == '__main__':
    items = [2, 2, 4, 6, 3]
    values = [3, 4, 8, 9, 6]
    backpack_max_weight = 9

    print(knapsack4(items, values, backpack_max_weight))
