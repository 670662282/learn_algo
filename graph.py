from queue import Queue


class Graph:
    def __init__(self, vertex_nums=4):
        """
        邻接矩阵 无向图
        """
        self.adjacency_matrix = [[] for _ in range(vertex_nums)]

    def add_edge(self, vertex_1, vertex_2):
        self.adjacency_matrix[vertex_1].append(vertex_2)
        self.adjacency_matrix[vertex_2].append(vertex_1)


def bfs(adj, start, end):
    result = []
    if start == end:
        return

    # visited 是用来记录已经被访问的顶点
    visited = [False] * len(adj)
    visited[start] = True

    # 用来记录搜索路径。当我们从顶点 s 开始，广度优先搜索到顶点 t 后，prev 数组中存储的就是搜索的路径。
    prev = [-1] * len(adj)

    # 用来存储已经被访问、但相连的顶点还没有被访问的顶点
    queue_ = Queue()
    queue_.put_nowait(start)

    while not queue_.empty():
        vertex = queue_.get()

        # 遍历队列中的顶点 连接的其他顶点
        # 如果某个顶点没有被访问， 那么就记录路径
        # 如果是目标value，就打印路径并返回
        # 不然则标记顶点访问并把这个顶点放入队列中
        for other_vertex in adj[vertex]:
            if visited[other_vertex] is False:
                prev[other_vertex] = vertex

                # 找到了
                if other_vertex == end:
                    print_bfs(prev, start, end, result)
                    return result

                visited[other_vertex] = True
                queue_.put_nowait(other_vertex)

    return result


def print_bfs(prev, start, end, result):
    """从尾递归到开始位置
    """
    if prev[end] != -1 and start != end:
        print_bfs(prev, start, prev[end], result)
        result.append((prev[end], end))
        print(f' {prev[end]} -> {end}')


found = False


def dfs(adj, start, end):
    result = []
    # visited 是用来记录已经被访问的顶点
    visited = [False] * len(adj)
    # 用来记录搜索路径。当我们从顶点 s 开始，广度优先搜索到顶点 t 后，prev 数组中存储的就是搜索的路径。
    prev = [-1] * len(adj)

    recur_dfs(adj, start, end, visited, prev)

    print_bfs(prev, start, end, result)
    return result


def recur_dfs(adj, start, end, visited, prev):
    global found
    # 如果已经找到 回溯的时候 直接true
    if found is True:
        return
    print(f'visited[{start}]')

    visited[start] = True

    # 找到了
    if start == end:
        found = True
        print('find it')
        return

    # 遍历start顶点 连接的其他顶点
    # 如果这个顶点没有被访问， 那么就记录路径
    # 并 已这个没有访问过的顶点 进行 继续递归
    for other_vertex in adj[start]:

        if visited[other_vertex] is False:
            prev[other_vertex] = start
            recur_dfs(adj, other_vertex, end, visited, prev)


if __name__ == '__main__':
    g = Graph(9)
    g.add_edge(0, 1)
    g.add_edge(0, 3)
    g.add_edge(1, 2)
    g.add_edge(1, 4)
    g.add_edge(2, 5)
    g.add_edge(3, 4)
    g.add_edge(4, 5)
    g.add_edge(4, 6)
    g.add_edge(5, 7)
    g.add_edge(6, 7)
    g.add_edge(3, 8)

    r = bfs(g.adjacency_matrix, 0, 7)
    print(r)
    print()
    print(dfs(g.adjacency_matrix, 0, 8))
