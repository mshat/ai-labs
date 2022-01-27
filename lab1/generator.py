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
        new_school_expansion = f'class {name}NewSchool({name}):\n    pass'
        old_school_expansion = f'class {name}OldSchool({name}):\n    pass'
        with_lyrics_new_school_expansion = f'class {name}NewSchoolWithLyrics({name}NewSchool):\n    pass'
        with_lyrics_old_school_expansion = f'class {name}OldSchoolWithLyrics({name}OldSchool):\n    pass'
        beats_new_school_expansion = f'class {name}NewSchoolBeats({name}NewSchool):\n    pass'
        beats_old_school_expansion = f'class {name}OldSchoolBeats({name}OldSchool):\n    pass'
        extended_leafs.append(new_school_expansion)
        extended_leafs.append(old_school_expansion)
        extended_leafs.append(with_lyrics_new_school_expansion)
        extended_leafs.append(with_lyrics_old_school_expansion)
        extended_leafs.append(beats_new_school_expansion)
        extended_leafs.append(beats_old_school_expansion)
    return extended_leafs


# leafs = get_leafs()
# print(leafs)
# print(len(leafs))

extended_leafs = generate_extended_leafs()
for leaf in extended_leafs:
    print(f'{leaf}\n\n')
print()
