import main
import sys
import inspect


def get_leafs():
    exclude_names = ['Genre']
    clsmembers = inspect.getmembers(sys.modules["main"], inspect.isclass)
    base_classes = {cls.__bases__[0] for name, cls in clsmembers}
    leafs = [(name, cls) for name, cls in clsmembers if cls not in base_classes and name not in exclude_names]
    return leafs


def generate_extended_leafs():
    leafs = get_leafs()
    extended_leafs = []
    for name, cls in leafs:
        vocal_expansion = f'class {name}Vocal({name}):\n    pass'
        beat_expansion = f'class {name}Beat({name}):\n    pass'
        extended_leafs.append(vocal_expansion)
        extended_leafs.append(beat_expansion)
    return extended_leafs


# leafs = get_leafs()
# print(leafs)
# print(len(leafs))

extended_leafs = generate_extended_leafs()
for leaf in extended_leafs:
    print(f'{leaf}\n\n')
print()
