import enum


class SexFilter(enum.Enum):
    any = 'anysex'
    female = 'female'
    male = 'male'


class GroupTypeFilter(enum.Enum):
    any = 'any'
    solo = 'solo'
    duet = 'duet'
    group = 'group'