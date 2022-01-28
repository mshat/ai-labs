from visual_tree import VisualNode


if __name__ == '__main__':
    node1 = VisualNode(1, [VisualNode(4), VisualNode(5)])
    node2 = VisualNode(2, [VisualNode(6), VisualNode(7)])
    node3 = VisualNode(3, [VisualNode(8), VisualNode(9)])
    root = VisualNode(0, [node1, node2])

    root.render_tree()