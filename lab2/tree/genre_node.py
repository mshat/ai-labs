from .visual_node import VisualNode

ARTISTS = ['name1', 'name2', 'name3']
NATIONALITIES = ['n1', 'n2', 'n3']


class GenreVisualNode(VisualNode):
    def __init__(self, name, year_of_birth, group_members_num, nationality, is_male=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.male_or_female = 1 if is_male else 0
        self.name = name
        assert name in ARTISTS
        self.nationality = nationality
        self.year_of_birth = year_of_birth
        self.group_members_number = group_members_num

    @property
    def solo_duet_group(self):  # категорийный
        if self.group_members_number == 1:
            return 'solo'
        elif self.group_members_number == 2:
            return 'duet'
        elif self.group_members_number > 2:
            return 'group'
        else:
            raise ValueError('Group_members_number must be > 0')

    @property
    def attributes(self) -> list:
        attributes = []
        male_female = (self.male_or_female + 1) / 2
        attributes.append(male_female)
