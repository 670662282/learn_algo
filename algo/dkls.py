def find_lowest_cost_node(costs):
    lowest_code = float("inf")
    lowest_code_node = None
    for node in costs:
        cost = costs[node]
        if cost < lowest_code and node not in processed:
            lowest_code = cost
            lowest_code_node = node

    return lowest_code_node


if __name__ == '__main__':
    graph = {}
    graph['start'] = {}
    graph['start']['a'] = 6
    graph['start']['b'] = 2

    graph["a"] = {}
    graph["a"]["fin"] = 1

    graph["b"] = {}
    graph["b"]["a"] = 3
    graph["b"]["fin"] = 5

    # 终点没有任何邻居
    graph["fin"] = {}

    infinity = float("inf")

    # store every one cost
    costs = {"a": 6, "b": 2, "fin": infinity}

    parents = {"a": "start", "b": "start", "fin": None}

    processed = []

    node = find_lowest_cost_node(costs)
    while node is not None:
        cost = costs[node]
        neighbors = graph[node]
        for n in neighbors.keys():
            new_cost = cost + neighbors[n]
            if costs[n] > new_cost:
                costs[n] = new_cost
                parents[n] = node
        processed.append(node)
        node = find_lowest_cost_node(costs)
    print(costs)
