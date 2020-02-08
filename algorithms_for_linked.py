from linked import MyLinkNode


def link_node_merge(link_1, link_2):
    # todo
    # 两个有序的链表合并
    # 如果一个节点的尾节点 小于 另外节点的首节点 ，直接小 拼接 大
    # 递归进行
    if link_1.is_empty():
        return link_2
    if link_2.is_empty():
        return link_1

    if link_1.first_node.value < link_2.first_node.value:
        node = link_node_merge(link_1.first_node.next, link_2)
        return link_1
    else:
        node = link_node_merge(link_1, link_2.first_node.next)
        return link_2


def link_node_median():
    link_node = MyLinkNode(1, 2, 3, 4, 5, 6, 7)
    fast_p = link_node.first_node
    slow_p = fast_p

    while fast_p.next != link_node.head:
        slow_p = slow_p.next
        fast_p = fast_p.next.next

    return slow_p.value


def is_hoop_link():
    link_node = MyLinkNode(1, 2, 3, 4, 5)
    fast_p = link_node.first_node
    slow_p = fast_p

    # 当快指针的速度是慢指针的2倍的时候， 会在慢指针跑完第一圈的时候相遇
    while slow_p != link_node.head:
        slow_p = slow_p.next
        # fast_head 跳过一轮的时候需要越过head节点
        if fast_p == link_node.head or fast_p.next == link_node.head:
            fast_p = fast_p.next.next.next
        else:
            fast_p = fast_p.next.next
        if slow_p == fast_p:
            return True
        continue

    return False


if __name__ == '__main__':
    print(is_hoop_link())
    print(link_node_median())

    link_node = MyLinkNode(1, 3, 5, 7, 9, 10)
    link_node_2 = MyLinkNode(2, 4, 6, 8)
    x = link_node_merge(link_node, link_node_2)
