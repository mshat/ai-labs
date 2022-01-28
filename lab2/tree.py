class Node:
    def __init__(self, val: int = 0, children: list = None):
        self.value = val
        self.children = children

    @property
    def values_str(self):
        return str(self.value)

    def __str__(self):
        return f'node {self.value}'


def show_tree(root: Node, spaces_num: int = 0):
    print(f"{'-' * spaces_num}{root.values_str}")
    if not root.children:
        return
    for child in root.children:
        show_tree(child, spaces_num + 1)




