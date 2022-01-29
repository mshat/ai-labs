from .node import Node


def find_path_to_node(root: Node, path, node_name):
    if root is None:
        return

    path.append(root.value)

    if root.value == node_name:
        return path

    for child in root.children:
        if find_path_to_node(child, path, node_name):
            return path

    path.pop()
    return


def calc_distance_between_nodes(root, node_name1, node_name2):
    if root:
        path1 = find_path_to_node(root, [], node_name1)
        path2 = find_path_to_node(root, [], node_name2)

        i = 0
        while i < len(path1) and i < len(path2):
            if path1[i] != path2[i]:
                break
            i = i + 1

        return len(path1) + len(path2) - 2 * i
    else:
        return 0
