class TrieNode:
    children = [None] * 26
    data = '/'
    is_ending_char = False


def insert(root, data):
    current = root
    for i in data:
        index = data[i] - 'a'
        if current.children[index] is None:
            node = TrieNode()
            node.data = i
            current.children[index] = node
        current = current.children[index]

    current.is_ending_char = True


def find(root, data):
    current = root
    for i in data:
        index = data[i] - 'a'
        if current.children[index] is None:
            return False
        current = current.children[index]

    if current.is_ending_char is True:
        return True
    else:
        return False


if __name__ == '__main__':
    root = TrieNode()
