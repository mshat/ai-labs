import enum

genres = [
    'trap',
    'mumble',
    'drill',
    'cloud',
    'underground',
    'freestyle',
    'gangsta rap',
    'hookah',
    'hardcore',
    'pop',
    'rap-rock',
    'rap-metal',
    'rapcore',
    'alternative hip hop',
    'g-funk',
    'nerdcore',
    'jazz-rap',
    'industrial hip hop',
    'comedy rap',
    'lo-fi hip hop',
    'conscious hip hop',
    'political hip hop',
    'battle rap',
    'trap-metal',
    'fonk',
    'horror',
    'emo',
]

Genre = enum.Enum(
    value='Genre',
    names=[(genre, i) for i, genre in enumerate(genres)],
)


class HipHop:
    def __init__(self):
        self.male_or_female: bool  # бинарный
        self.name: str  # непереводимый (тэг)
        self.nationality: str  # непереводимый (тэг)
        self.year_of_birth: int  # количественный
        self.solo_duet_group: enum.Enum  # категорийный


class ElectronicHipHop(HipHop):
    pass


class Trap(HipHop):
    """
    Поджанр хип-хопа
    В музыке широко используются многослойные синтезаторы, на которых ведётся мелодия с жёсткой линией;
    хрустящие, грязные и ритмичные рабочие барабаны; глубокие барабаны-бочки, либо мощные суббасовые партии;
    хай-хэты, ускоренные в два, три и более раз. Также применяются семплированные партии струнных, медно-духовых,
    клавишных инструментов, вырезанные из кинематографической и симфонической музыки, создающие общую тёмную, грубую,
    зловещую и мрачную атмосферу для слушателя. Темп типичного трэп-трека — в районе 140 ударов в минуту
    """
    pass


class Phonk(ElectronicHipHop):
    """
    поджанр хип-хопа, характеризуется ностальгическими семплами фанка, кассетным звучанием, взятым из LO-FI и часто
    аккомпанирующимися старыми вокальными записями в стиле Мемфис-рэпа. В жанре обычно используются хип-хоп семплы
    ранних 1990-х годов, соединённые с джазовыми мотивами
    """
    pass


class Cloud(ElectronicHipHop):
    """
    Клауд-рэп (дословно – «облачный рэп») – микрожанр хип-хоп-музыки. Обычно характеризуется замедленными
    («туманными») инструментальными партиями и лоу-фай звучанием (от английского low fidelity – низкое качество)
    """
    pass


class Drill(ElectronicHipHop):
    """
    поджанр хип-хопа, отличается тёмной, мрачной подачей и стороной лирического содержания трэп-музыки.
    Дрилл отличается мрачными текстами про насилие и жизнь уличных банд.
    """
    pass


class Mumble(ElectronicHipHop):
    """
    бормочущий рэп, мямля-рэп» — поджанр трэп-музыки.Характеризуется упором на выразительность звучания, в отличие от
    традиционного хип-хопа, в основе которого лежит лирика и рифмы
    """


class Battle(HipHop):
    """
    Рэп-баттл (варианты: рэп-битва) — состязание двух исполнителей в жанре рэп при помощи специального рифмосложения.
    В классическом понимании рэп-баттл подразумевает словесный поединок между рэп-исполнителями
    """
    pass


class FreestyleBattle(Battle):
    """
    Фристайл-баттл — подразумевает под собой выступление МС без заготовленного текста.
    Таким образом оценивается не только количество рифм и качество ударных линий (панчей),
    но и умение быстро импровизировать, рифмуя буквально на ходу.
    """
    pass


class RegularBattle(Battle):
    """
    В отличии от фристайла, текст готоовится заранее и выучивается
    """
    pass


class Hardcore(HipHop):
    """
    Хардкор-хип-хоп характеризуется агрессией и конфронтацией и обычно описывает насилие или гнев
    """
    pass


class Gangsta(Hardcore):
    """
    Cтиль хип-хопа, характеризующийся темами и текстами, которые обычно подчёркивают стиль жизни «гангстера».
    """
    pass


class Horrorcore(Hardcore):
    """
    Хоррорко́р (англ. Horrorcore) — поджанр хип-хоп музыки, его лирическое содержание основывается на
    образах фильмов ужасов, а может быть ещё более пугающим, описывающим самые низменные пороки человеческой натуры,
    ничем не прикрытое насилие. Хотя биты хорроркора представляют собой продукт семплирования, в последнее время многие
    исполнители стали насыщать свои композиции тяжёлыми гитарными риффами, благодаря чему звучание треков представляет
    собой смесь дэт-метала и речитатива.
    """
    pass


class Alternative(HipHop):
    """
     поджанр хип-хоп-музыки, охватывающий широкий спектр стилей, которые обычно не считаются мейнстримом. AllMusic
     определяет его следующим образом: «Альтернативный рэп относится к хип-хоп-группам, которые отказываются
     соответствовать каким-либо традиционным стереотипам рэпа, таким как гангста-рэп, Miami bass[en], хардкор-хип-хоп,
     поп-рэп и рэп для вечеринок[en]. Вместо этого группы размывают жанры, в равной степени опираясь на фанк и поп-рок,
     а также джаз, соул, регги и даже фолк-музыку».
    """
    pass


class Emo(Alternative):
    """
    поджанр хип-хопа и эмо-музыки, характеризующийся сочетанием хип-хопа с элементами таких жанров рок-музыки, как
    инди-рок, поп-панк и ню-метал, обычно встречающимися в эмо-музыке.
    """


class RapRock(Alternative):
    """
    жанр, который сочетает в себе вокальные и инструментальные элементы хип-хопа с различными формами рок-музыки
    """
    pass


class PlaceHolderGenre(HipHop):
    pass


class Hookah(PlaceHolderGenre):
    """
    * В музыке также характерно использование традиционных хип-хоповых битов. В ряде треков, тем не менее,
    используется прямая бочка.
    * Речитатив в кальян-рэпе звучит, как правило, мягче, в стилистике отмечается влияние такого жанра, как мейхана.
    * Также в ряде треков отмечается наличие чистого вокала в стилистике, схожей с соулом.
    * Тематика песен несхожа с традиционным хип-хопом и нехарактерна для него. Как правило, это темы, характерные
    для поп-музыки в целом: неразделенная любовь, мечты о счастье. В некоторых треках отмечается романтика
    «клубной» жизни. В целом, тематика текстов достаточно разнообразна.
    """
    pass


class Pop(PlaceHolderGenre):
    """
    Поп-рэп — гибрид хип-хопа с массивным мелодичным заполнением, который традиционно является частью хоровой секции
    в структуре обычной поп-композиции[4]. Поп-рэп имеет тенденцию к понижению злости и увеличению лирической ценности
    по сравнению с уличным рэпом
    """
    pass


class Underground(PlaceHolderGenre):
    pass
