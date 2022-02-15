import re
from enum import Enum

import pandas as pd
import pymorphy2

import melody
import paramSearch
from proximity import measureMethod
from tools import HarmonicType, Complexity, Tonality, Genre

morph = pymorphy2.MorphAnalyzer()


class MsgMood(Enum):
    QUESTION = 1
    REQUEST = 2
    RATING = 3
    UNDEFINED = 4

class DialogState:
    NOTHING = 1
    WAITING_REACTION = 2

class UserData:
    username: str
    dislikes: []
    melodies: []
    history: []
    acceptPorog: int

    def __init__(self):
        data = pd.read_json("../test.json")
        self.melodies = []
        for item in data.iterrows():
            item = item[1]
            curMelody = melody.Melody(HarmonicType.DIATONIC, Tonality[item['Tonality']['name']],
                                   Complexity[item['Complexity']['name']],
                                   item['HasBends_Bool'], item['IsRussian_Bool'], Genre[item['Genre']['name']],
                                   item['Performer'], item['Name'])
            self.melodies.append(curMelody)
        self.dislikes = len(self.melodies) * [0]

        self.history = []
        self.username = 'Gek'
        self.acceptPorog = 75
        # self.acceptPorog = 60

class DialogContext:
    user: UserData
    state: DialogState
    lastRecArr: []
    lastRecInd: int

    def __init__(self):
        self.user = UserData()
        self.state = DialogState.NOTHING
        self.lastRecInd = -1
        self.lastRecArr = []

class TestInput_1:
    msg: str
    answer: str
    mood: MsgMood

def NewTestInput_1(msg):
    test = TestInput_1()
    test.msg = msg
    return test

def pos(word, morth=pymorphy2.MorphAnalyzer()):
    return morth.parse(word)[0].tag.POS

def clearMsg(msg):
    words = msg.split()
    if words[-1][-1] == '?':
        words[-1] = words[-1][:-1]
    functors_pos = {'INTJ', 'CONJ', 'PREP', 'NPRO'}  # междометия, союзы, предлоги
    return ' '.join([word for word in words if pos(word) not in functors_pos])

def findGoal(msg):
    words = msg.split()
    functors_pos = {'VERB', 'INFN'}  # междометия, союзы, предлоги
    return ' '.join([word for word in words if pos(word) not in functors_pos])

def clearFromWord(msg, word):
    return " ".join(filter(lambda x: word not in x, msg.split()))

def defineMood(msg, dCtx):

    if dCtx.state == DialogState.NOTHING:
        # split on words
        words = msg.split()
        # find verbs
        verbs = []
        for word in words:
            ind = 0
            parsedWordVariants = morph.parse(word)
            parsedWord = parsedWordVariants[ind]
            # INFN doesn`t have mood. Try to find VERB
            if parsedWord.tag.POS == 'INFN' and len(verbs) == 0:
                ind += 1
                while(parsedWord.tag.POS != 'VERB' and ind < len(parsedWordVariants)):
                    parsedWord = parsedWordVariants[ind]
                    ind += 1
            if parsedWord.tag.POS == 'VERB':
                verbs.append(parsedWord)

        # define mood
        if len(verbs) == 0:
            if msg[len(msg) - 1] == '?':
                return MsgMood.QUESTION
            return MsgMood.RATING
        if len(verbs) == 1:
            verb = verbs[0]
            if verb.tag.mood == 'indc' and msg[len(msg) - 1] == '?':
                return MsgMood.QUESTION
            if verb.tag.mood == 'impr':
                return MsgMood.REQUEST
            return MsgMood.UNDEFINED

        if verbs[0].tag.mood == 'indc' and msg[len(msg) - 1] == '?':
            return MsgMood.QUESTION
        if verbs[0].tag.mood == 'impr':
            return MsgMood.REQUEST
        return MsgMood.UNDEFINED
    elif dCtx.state == DialogState.WAITING_REACTION:
        return MsgMood.RATING

def solveQuestion(msg, dCtx):
    exist = '(есть|имеются|в наличии|знаешь|найди|хочу)'
    clearedMsg = clearMsg(msg)
    result = re.findall(exist, clearedMsg, re.IGNORECASE)
    if len(result) > 0:
        before_keyword, keyword, after_keyword = clearedMsg.partition(result[0])
        clearedAfterKey = findGoal(after_keyword)
    else:
        clearedAfterKey = findGoal(clearedMsg)

    clearedAfterKey = lemmatize(clearedAfterKey)
    rusOk, rusMatch = solveRussian(clearedAfterKey)
    rusMean = ''
    if rusOk:
        rusMean = 1
        clearedAfterKey = clearFromWord(clearedAfterKey, rusMatch)

    genreOk, genreMatch = solveGenre(clearedAfterKey)
    genre = ''
    if genreOk:
        clearedAfterKey = clearFromWord(clearedAfterKey, genreMatch)

        if genreMatch == 'рок':
            genre = Genre.Rock
        elif genreMatch == 'регги':
            genre = Genre.Reggae
        elif genreMatch == 'блюз':
            genre = Genre.Blues
        elif genreMatch == 'народ' or genreMatch == 'фолк':
            genre = Genre.Folk
        elif genreMatch == 'поп':
            genre = Genre.Pop
        elif genreMatch == 'кантри':
            genre = Genre.Country


    m = melody.Melody(HarmonicType.DIATONIC, '', '', '', rusMean, genre, '', '')
    res = paramSearch.findByFilterParams(dCtx.user.melodies, m, clearedAfterKey)

    return res

def solveRecommendation(msg, dCtx):
    recommend = '(посоветовать|советовать|подсказать|порекоммендовать|давать|дать)'
    clearedMsg = clearMsg(lemmatize(msg))
    result = re.findall(recommend, clearedMsg, re.IGNORECASE)
    if len(result) == 0:
        return [], 0
    before_keyword, keyword, after_keyword = clearedMsg.partition(result[0])
    clearedAfterKey = findGoal(after_keyword)

    clearedAfterKey = lemmatize(clearedAfterKey)
    rusOk, rusMatch = solveRussian(clearedAfterKey)
    rusMean = 0
    if rusOk:
        rusMean = 1
        clearedAfterKey = clearFromWord(clearedAfterKey, rusMatch)

    genreOk, genreMatch = solveGenre(clearedAfterKey)
    genre = Genre.Rock
    if genreOk:
        clearedAfterKey = clearFromWord(clearedAfterKey, genreMatch)

        if genreMatch == 'рок':
            genre = Genre.Rock
        elif genreMatch == 'регги':
            genre = Genre.Reggae
        elif genreMatch == 'блюз':
            genre = Genre.Blues
        elif genreMatch == 'народ' or genreMatch == 'фолк':
            genre = Genre.Folk
        elif genreMatch == 'поп':
            genre = Genre.Pop
        elif genreMatch == 'кантри':
            genre = Genre.Country


    perfVariants = paramSearch.findPerformer(dCtx.user.melodies, clearedAfterKey)
    if len(perfVariants) == 0:
        m = melody.Melody(HarmonicType.DIATONIC, Tonality.C, Complexity.BEGINNER, 0, rusMean, genre, '', '')
        res = measureMethod(dCtx.user.melodies, dCtx.user.dislikes, m, 'simpson', 28, False)
        return res, 0
    else:
        for perf in perfVariants:
            m = melody.Melody(HarmonicType.DIATONIC, Tonality.C, Complexity.BEGINNER, 0, rusMean, genre, perf, '')
            m = paramSearch.fillEmptyParamsByPerformer(dCtx.user.melodies, m)
            res = measureMethod(dCtx.user.melodies, dCtx.user.dislikes, m, 'simpson', 28, True)
            return res, 0

def solveRating(msg, dCtx):
    positive_100 = '(что нужно|отлично|класс)'
    positive_90 = '(хорошо|спасибо)'
    positive_70 = '(норм|нормально)'
    positive_60 = '(покатит|неплохо|пойдёт|сойдёт|ничего)'
    negative40 = '(неочень)'
    negative30 = '(так себе)'
    negative10 = '(плохо)'
    negative0 = '(нет|хрень|фигня|отстой|фу|паршиво|другую|другое)'

    positive100Res = re.search(positive_100, msg, re.IGNORECASE)
    positive90Res = re.search(positive_90, msg, re.IGNORECASE)
    positive70Res = re.search(positive_70, msg, re.IGNORECASE)
    positive60Res = re.search(positive_60, msg, re.IGNORECASE)
    negative40Res = re.search(negative40, msg, re.IGNORECASE)
    negative30Res = re.search(negative30, msg, re.IGNORECASE)
    negative10Res = re.search(negative10, msg, re.IGNORECASE)
    negative0Res = re.search(negative0, msg, re.IGNORECASE)

    wantEasy = '(попроще|сложно)'
    wantEasyRes = re.search(wantEasy, msg, re.IGNORECASE)
    if wantEasyRes:
        print('Ладно, держи попроще')
        dCtx.lastRecInd = dCtx.lastRecInd + 1
        print(dCtx.lastRecArr[dCtx.lastRecInd])
        print('Как Вам?')
        return False

    wantHard = '(посложнее|просто|скучно)'
    wantHardRes = re.search(wantHard, msg, re.IGNORECASE)
    if wantHardRes:
        print('Ладно, держи посложнее')
        dCtx.lastRecInd = dCtx.lastRecInd + 1
        print(dCtx.lastRecArr[dCtx.lastRecInd])
        print('Как Вам?')
        return False

    if positive100Res:
        getAcceptPorog = 100
    elif positive90Res:
        getAcceptPorog = 90
    elif positive70Res:
        getAcceptPorog = 70
    elif positive60Res:
        getAcceptPorog = 60
    elif negative40Res:
        getAcceptPorog = 40
    elif negative30Res:
        getAcceptPorog = 30
    elif negative10Res:
        getAcceptPorog = 10
    elif negative0Res:
        getAcceptPorog = 0
    else:
        print('Не понял Вас.. Как Вам прошлая рекомендация?')
        return False

    if getAcceptPorog < dCtx.user.acceptPorog:
        if len(dCtx.lastRecArr) > dCtx.lastRecInd + 1:
            print('Ладно, как тебе тогда эта?')
            dCtx.lastRecInd = dCtx.lastRecInd + 1
            print(dCtx.lastRecArr[dCtx.lastRecInd])
            return False
        else:
            print('Больше нечего рекомендовать')
            return True

    print('Ну, и хорошо')
    return True



def solveGenre(msg):
    genres = '(рок|регги|джаз|блюз|народ|фолк|соул|поп|кантри)'
    g = re.search(genres, msg, re.IGNORECASE)
    if g:
        return True, g.group(0)
    return False, ''

def solveComplexity(msg):
    complex = '(простой|сложный)'
    c = re.search(complex, msg, re.IGNORECASE)
    if c:
        return True, c.group(0)
    return False, ''

def solveRussian(msg):
    russian = ('русский|отечественный|наш')
    r = re.search(russian, msg, re.IGNORECASE)
    if r:
        return True, r.group(0)
    return False, ''

def solveMsg(msg, dCtx):
    msg = msg.lower()
    mood = defineMood(msg, dCtx)
    if dCtx.state == DialogState.NOTHING:
        if mood == MsgMood.QUESTION:
            res = solveQuestion(msg, dCtx)
            if len(res) > 0:
                print(res)
            else:
                print('Не могу понять, что Вам нужно..')

        elif mood == MsgMood.REQUEST:
            dCtx.lastRecArr, dCtx.lastRecInd = solveRecommendation(msg, dCtx)
            if len(dCtx.lastRecArr) > 0:
                dCtx.state = DialogState.WAITING_REACTION
                print(dCtx.lastRecArr[dCtx.lastRecInd])
                print('Ну как?')
            else:
                print('Не могу понять, что Вам нужно..')
        else:
            print('Не понял цели Вашего сообщения :(')
    elif dCtx.state == DialogState.WAITING_REACTION:
        res = solveRating(msg, dCtx)
        if res:
            dCtx.state = DialogState.NOTHING

def lemmatize(msg):
    words = msg.split() # разбиваем текст на слова
    res = list()
    for word in words:
        ps = morph.parse(word)
        p = morph.parse(word)[0]
        res.append(p.normal_form)

    return ' '.join(res)

if __name__ == '__main__':

    dCtx = DialogContext()

    test1Arr = [
        NewTestInput_1('А есть beatles?'),
        NewTestInput_1('Есть beatles?'),
        NewTestInput_1('Есть что-нибудь из beatles?'),
        NewTestInput_1('У тебя есть beatles?'),
        NewTestInput_1('А знаешь что-нибудь из beatles?'),
        NewTestInput_1('Знаешь Yesterday?'),
        NewTestInput_1('Найди Yesterday'),
        NewTestInput_1('Хочу попробовать Yesterday'),
        NewTestInput_1('Есть beatles Yesterday?'),
        NewTestInput_1('Есть что-нибудь из несложного русского рока?'),
        NewTestInput_1('Есть что-нибудь из Караганды?'),
    ]

    test2Arr = [
        NewTestInput_1('Посоветуй что-нибудь для меня'),
        NewTestInput_1('Порекоммендуй что-нибудь из русского рока.'),
        NewTestInput_1('Подскажи что-нибудь из beatles?'),
        NewTestInput_1('Подскажи что-нибудь блюзовое'),
    ]

    while True:
        msg = input()
        solveMsg(msg, dCtx)