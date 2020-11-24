def quick_sort(lists):
    print(lists)
    if len(lists) < 2:
        return lists
    else:
        pivot = lists[0]

        less = [i for i in lists[1:] if i <= pivot]
        greater = [i for i in lists[1:] if i > pivot]

        return quick_sort(less) + [pivot] + quick_sort(greater)


if __name__ == '__main__':
    print(quick_sort([10, 5, 2, 3, 9]))
