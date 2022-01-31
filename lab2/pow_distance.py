from tree.genre_node import VisualNode, GenreVisualNode


def pow_distance(node1: GenreVisualNode, node2: GenreVisualNode, power):
    distance = 0
    print(node1.countable_attributes, node2.countable_attributes)
    for i in range(len(node1.countable_attributes)):
        distance += pow(abs(node1.countable_attributes[i] - node2.countable_attributes[i]), power)
    return pow(distance, 1/power)


