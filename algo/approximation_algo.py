
if __name__ == '__main__':
    states_needed = {"mt", "wa", "or", "id", "nv", "ut", "ca", "az"}

    stations = {
        "kone": {"id", "nv", "ut"},
        "ktwo": {"wa", "id", "mt"},
        "kthree": {"or", "nv", "ca"},
        "kfour": {"nv", "ut"},
        "kfive": {"ca", "az"}
    }

    final_stations = set()
    # 遍历所有的广播台，从中选
    # 择覆盖了最多的未覆盖州的广播台。

    while states_needed:
        best_station = None
        states_covered = set()

        for station, states_for_station in stations.items():
            covered = states_needed & states_for_station
            if len(covered) > len(states_covered):
                best_station = station
                states_covered = covered

        states_needed -= states_covered
        final_stations.add(best_station)

    print(final_stations)