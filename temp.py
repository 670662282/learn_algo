def binary_search(list_, item):
    low = 0
    high = len(list_) - 1

    while low <= high:
        mid = (low + high) // 2

        if list_[mid] == item:
            return mid

        if list_[mid] < item:
            low = mid

        if list_[mid] > item:
            high = mid

    return None


