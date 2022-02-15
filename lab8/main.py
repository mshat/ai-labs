from parsers import SentenceParser, Word, Sentence

# import melody
# import paramSearch
# from proximity import measureMethod
# from tools import HarmonicType, Complexity, Tonality, Genre


class DialogContext:
#     user: UserData
#     state: DialogState
#     lastRecArr: []
#     lastRecInd: int

    def __init__(self):
        # self.user = UserData()
        # self.state = DialogState.NOTHING
        self.lastRecInd = -1
        self.lastRecArr = []


if __name__ == '__main__':
    dialog_context = DialogContext()
    msg = 'Есть что-нибудь из несложного русского рока?'
    msg = 'найди похожих исполнителей на Noize mc'
    sentence = SentenceParser(msg).parse()
    print(sentence)


    # while True:
    #     msg = input('--> ')
    #     solveMsg(msg, dCtx)