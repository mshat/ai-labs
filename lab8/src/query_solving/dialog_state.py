import enum


class DialogState(enum.Enum):
    start = 1
    search = 2
    filter = 3
    count_filter = 4
    number = 5
    like = 6
    dislike = 7
    info = 8