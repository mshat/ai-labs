# ARTISTS = ['лигалайз', 'многоточие', 'krec', 'guf', 'баста', 'каста', 'ак-47', 'каспийский груз', 'кровосток', 'the chemodan', 'смоки мо', 'рем дигга', 'миша маваши', 'd-man 55', 'грот', 'oxxxymiron', 'соня мармеладова', 'alyona alyona', 'sid', 'redo', 'ram', 'полумягкие', 'оу74', 'паша техник', 'овсянкин', 'pharaoh', 'boulevard depo', 'mnogoznaal', 'kizaru', 'лсп', 'atl', 'макс корж', 'slava marlow', 'скриптонит', 'noize mc', 'loqiemean', 'anacondaz', '25/17', 'lizer', 'джизус', 'мукка', 'lizer', 'face', 'gone.fludd', 'big baby tape', 'элджей', 'morgenshtern', 'rakhim', 'егор крид', 'тимати', 'pyrokinesis', 't-fest', 'miyagi', 'jah khalib', 'hammali & navai']
# GENRES = ['freestyle', 'regular', 'emo', 'raprock', 'cloud', 'club', 'drill', 'electronicvocal', 'grime', 'mumble', 'phonk', 'hardcore', 'horrorcore', 'underground', 'hookah', 'pop', 'gangsta', 'workout', 'classic', 'soft']

keywords = {
    'search': ('найти', 'похожий', 'схожий', 'как',),
    'artist': ('артист', 'исполнитель', 'музыкант', 'рэпер', 'певец'),
    'genre': ('жанр', 'стиль',),

    'about': ('о', 'про'),

    'recommend': ('посоветовать', 'порекомендовать',),
    'show': ('показывать', 'показать', 'выводить', 'вывести'),
    'include': ('оставить', 'оставлять', 'добавить', 'включить', 'прибавить', 'выбрать'),
    'exclude': ('убрать', 'исключать', 'исключить', 'отмести', 'отметать', 'выкинуть', 'выкидывать', 'отсеить', 'отсеивать', 'удалять', 'удалить', 'удаль', 'удали'),
    'all': ('весь', 'всё'),
    'year': ('год',),
    'older': ('старший', 'большой', 'за', 'от'),
    'younger': ('младший', 'маленький', 'до'),
    'range': ('между', 'диапазон',),
    'solo': ('соло',),
    'duet': ('дуэт',),
    'group': ('группа',),
    'age': ('возраст',),

    'talk about': ('рассказать',),
    'info': ('информация', 'узнать'),  # мб добавить "про|об" артиста и тд

    'like': ('нравиться', 'лайк', 'любить', 'любимый', 'лайковый',),

    'dislike': ('не нравиться', 'дизлайк', 'не любить', 'нелюбимый', 'дизлайковый',),

    'how many': ('сколько',),
    'number': ('количество',),

    'restart': ('вернуться', 'начало', 'новый', 'начать', 'заново'),

    'filter': ('фильтр', 'ограничение',)
}

# for tag1, aliases1 in keywords.items():
#     for tag2, aliases2 in keywords.items():
#         if tag1 != tag2:
#             if set(aliases1) & set(aliases2):
#                 print(tag1, tag2, set(aliases1) & set(aliases2))

GENDERS = {
    'мужcкой': 'мужской',
    'мужского': 'мужской',
    'мужчин': 'мужской',
    'мужчина': 'мужской',
    'женский': 'женский',
    'женского': 'женский',
    'женщин': 'женский',
    'женщина': 'женский',
}

ARTISTS = {
    'лигалайз': 'лигалайз',
    'лигалайза': 'лигалайз',
    'лигалайзу': 'лигалайз',
    'лигалайзе': 'лигалайз',
    'многоточие': 'многоточие',
    'многоточия': 'многоточие',
    'многоточию': 'многоточие',
    'многоточии': 'многоточие',
    'krec': 'krec',
    'крек': 'krec',
    'крека': 'krec',
    'креку': 'krec',
    'креке': 'krec',
    'guf': 'guf',
    'гуф': 'guf',
    'гуфа': 'guf',
    'гуфу': 'guf',
    'гуфе': 'guf',
    'баста': 'баста',
    'басту': 'баста',
    'басте': 'баста',
    'каста': 'каста',
    'касту': 'каста',
    'касте': 'каста',
    'ак-47': 'ак-47',
    'каспийский груз': 'каспийский груз',
    'каспийского груза': 'каспийский груз',
    'каспийскому грузу': 'каспийский груз',
    'каспийском грузе': 'каспийский груз',
    'кровосток': 'кровосток',
    'кровостока': 'кровосток',
    'кровостоку': 'кровосток',
    'кровостоке': 'кровосток',
    'chemodan': 'the chemodan',
    'the chemodan': 'the chemodan',
    'чемодан': 'the chemodan',
    'чемодана': 'the chemodan',
    'чемодану': 'the chemodan',
    'чемодане': 'the chemodan',
    'смоки мо': 'смоки мо',
    'рем дигга': 'рем дигга',
    'рем дигги': 'рем дигга',
    'рем диггу': 'рем дигга',
    'рем дигге': 'рем дигга',
    'миша маваши': 'миша маваши',
    'мишу маваши': 'миша маваши',
    'мише маваши': 'миша маваши',
    'd-man 55': 'd-man 55',
    'грот': 'грот',
    'гроту': 'грот',
    'грота': 'грот',
    'гроте': 'грот',
    'oxxxymiron': 'oxxxymiron',
    'оксимирон': 'oxxxymiron',
    'оксимирона': 'oxxxymiron',
    'оксимирону': 'oxxxymiron',
    'оксимироне': 'oxxxymiron',
    'соня мармеладова': 'соня мармеладова',
    'соня мармеладову': 'соня мармеладова',
    'соню мармеладову': 'соня мармеладова',
    'соне мармеладовой': 'соня мармеладова',
    'alyona alyona': 'alyona alyona',
    'алёна алёна': 'alyona alyona',
    'алена алена': 'alyona alyona',
    'алену алену': 'alyona alyona',
    'алене алене': 'alyona alyona',
    'алёну алёну': 'alyona alyona',
    'алёне алёне': 'alyona alyona',
    'sid': 'sid',
    'сид': 'sid',
    'сида': 'sid',
    'сиду': 'sid',
    'сиде': 'sid',
    'redo': 'redo',
    'редо': 'redo',
    'рэдо': 'redo',
    'ram': 'ram',
    'рэм': 'ram',
    'рэма': 'ram',
    'рэму': 'ram',
    'рэме': 'ram',
    'полумягкие': 'полумягкие',
    'полумягких': 'полумягкие',
    'полумягким': 'полумягкие',
    'оу74': 'оу74',
    'паша техник': 'паша техник',
    'паши техника': 'паша техник',
    'пашу техника': 'паша техник',
    'паше технику': 'паша техник',
    'паше технике': 'паша техник',
    'овсянкин': 'овсянкин',
    'овсянкина': 'овсянкин',
    'овсянкину': 'овсянкин',
    'овсянкине': 'овсянкин',
    'pharaoh': 'pharaoh',
    'фараон': 'pharaoh',
    'фараона': 'pharaoh',
    'фараону': 'pharaoh',
    'фараоне': 'pharaoh',
    'boulevard depo': 'boulevard depo',
    'бульвар депо': 'boulevard depo',
    'бульвара депо': 'boulevard depo',
    'бульвару депо': 'boulevard depo',
    'бульваре депо': 'boulevard depo',
    'mnogoznaal': 'mnogoznaal',
    'многознал': 'mnogoznaal',
    'многознале': 'mnogoznaal',
    'многозналу': 'mnogoznaal',
    'многознала': 'mnogoznaal',
    'многознаал': 'mnogoznaal',
    'многознаале': 'mnogoznaal',
    'многознаалу': 'mnogoznaal',
    'многознаала': 'mnogoznaal',
    'kizaru': 'kizaru',
    'кизару': 'kizaru',
    'лсп': 'лсп',
    'atl': 'atl',
    'атл': 'atl',
    'атла': 'atl',
    'макс корж': 'макс корж',
    'макса коржа': 'макс корж',
    'максу коржу': 'макс корж',
    'максе корже': 'макс корж',
    'slava marlow': 'slava marlow',
    'слава мэрлоу': 'slava marlow',
    'славу мэрлоу': 'slava marlow',
    'славы мэрлоу': 'slava marlow',
    'славе мэрлоу': 'slava marlow',
    'скриптонит': 'скриптонит',
    'скриптоните': 'скриптонит',
    'скриптонита': 'скриптонит',
    'скриптониту': 'скриптонит',
    'noize mc': 'noize mc',
    'нойз мс': 'noize mc',
    'нойза мс': 'noize mc',
    'нойзу мс': 'noize mc',
    'нойзе мс': 'noize mc',
    'нойз': 'noize mc',
    'нойза': 'noize mc',
    'нойзе': 'noize mc',
    'нойзу': 'noize mc',
    'loqiemean': 'loqiemean',
    'локимин': 'loqiemean',
    'локимина': 'loqiemean',
    'локимину': 'loqiemean',
    'локимине': 'loqiemean',
    'anacondaz': 'anacondaz',
    'анакондаз': 'anacondaz',
    '25/17': '25/17',
    'lizer': 'lizer',
    'лизер': 'lizer',
    'лизере': 'lizer',
    'лизера': 'lizer',
    'лизеру': 'lizer',
    'джизус': 'джизус',
    'джизуса': 'джизус',
    'джизусу': 'джизус',
    'мукк': 'мукка',
    'мукка': 'мукка',
    'мукку': 'мукка',
    'мукке': 'мукка',
    'face': 'face',
    'фейс': 'face',
    'фэйс': 'face',
    'фэйе': 'face',
    'фейса': 'face',
    'фейсу': 'face',
    'фейсе': 'face',
    'фэйса': 'face',
    'фэйсу': 'face',
    'gone.fludd': 'gone.fludd',
    'гон флад': 'gone.fludd',
    'гон фладе': 'gone.fludd',
    'гон фладд': 'gone.fludd',
    'гон фладде': 'gone.fludd',
    'гон флада': 'gone.fludd',
    'гон фладда': 'gone.fludd',
    'гон фладу': 'gone.fludd',
    'гон фладду': 'gone.fludd',
    'big baby tape': 'big baby tape',
    'биг бейби тейп': 'big baby tape',
    'биг бейби тейпе': 'big baby tape',
    'биг бейби тейпу': 'big baby tape',
    'биг бэйби тейп': 'big baby tape',
    'биг бэйби тейпе': 'big baby tape',
    'биг бэйби тейпу': 'big baby tape',
    'биг бейби тэйп': 'big baby tape',
    'биг бейби тэйпе': 'big baby tape',
    'биг бейби тэйпу': 'big baby tape',
    'биг бэйби тэйп': 'big baby tape',
    'биг бэйби тэйпу': 'big baby tape',
    'биг бейби тейпа': 'big baby tape',
    'биг бэйби тейпа': 'big baby tape',
    'биг бейби тэйпа': 'big baby tape',
    'биг бэйби тэйпа': 'big baby tape',
    'биг бэйби тэйпе': 'big baby tape',
    'элджей': 'элджей',
    'элджея': 'элджей',
    'элджею': 'элджей',
    'элджее': 'элджей',
    'morgenshtern': 'morgenshtern',
    'моргенштерн': 'morgenshtern',
    'моргенштерна': 'morgenshtern',
    'моргенштерну': 'morgenshtern',
    'моргенштерне': 'morgenshtern',
    'rakhim': 'rakhim',
    'рахим': 'rakhim',
    'рахима': 'rakhim',
    'рахиму': 'rakhim',
    'рахиме': 'rakhim',
    'егор крид': 'егор крид',
    'егора крида': 'егор крид',
    'егору криду': 'егор крид',
    'егоре криде': 'егор крид',
    'тимати': 'тимати',
    'pyrokinesis': 'pyrokinesis',
    'пирокинезис': 'pyrokinesis',
    'пирокинезиса': 'pyrokinesis',
    'пирокинезису': 'pyrokinesis',
    'пирокинезисе': 'pyrokinesis',
    't-fest': 't-fest',
    'ти-фест': 't-fest',
    'ти-фесте': 't-fest',
    'ти-феста': 't-fest',
    'ти-фесту': 't-fest',
    'ти фест': 't-fest',
    'ти фесте': 't-fest',
    'ти феста': 't-fest',
    'ти фесту': 't-fest',
    'miyagi': 'miyagi',
    'мияги': 'miyagi',
    'jah khalib': 'jah khalib',
    'джа халиб': 'jah khalib',
    'джа халибе': 'jah khalib',
    'джа халиба': 'jah khalib',
    'джа халибу': 'jah khalib',
    'hammali & navai': 'hammali & navai',
    'хамали & наваи': 'hammali & navai',
    'хамали и наваи': 'hammali & navai',
}
GENRES = {
    'emo': 'emo',
    'эмо': 'emo',
    'raprock': 'raprock',
    'rap rock': 'raprock',
    'рэп рок': 'raprock',
    'рэп-рок': 'raprock',
    'реп рок': 'raprock',
    'реп-рок': 'raprock',
    'cloud': 'cloud',
    'клауд': 'cloud',
    'club': 'club',
    'клуб': 'club',
    'клубный': 'club',
    'drill': 'drill',
    'дрилл': 'drill',
    'electronicvocal': 'electronicvocal',
    'grime': 'grime',
    'грайм': 'grime',
    'mumble': 'mumble',
    'мамбл': 'mumble',
    'phonk': 'phonk',
    'фонк': 'phonk',
    'hardcore': 'hardcore',
    'хардкор': 'hardcore',
    'horrorcore': 'horrorcore',
    'хорроркор': 'horrorcore',
    'хороркор': 'horrorcore',
    'underground': 'underground',
    'андеграунд': 'underground',
    'hookah': 'hookah',
    'кальян': 'hookah',
    'кальянный': 'hookah',
    'pop': 'pop',
    'поп': 'pop',
    'gangsta': 'gangsta',
    'гангста': 'gangsta',
    'ганста': 'gangsta',
    'workout': 'workout',
    'воркаут': 'workout',
    'спортивный': 'workout',
    'спорт': 'workout',
}
