import enum


class SexFilter(enum.Enum):
    any = 'any_sex'
    female = 'female'
    male = 'male'


class GroupTypeFilter(enum.Enum):
    any = 'any'
    solo = 'solo'
    duet = 'duet'
    group = 'group'