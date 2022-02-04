import PySimpleGUI as sg
import interface

layout = [
    [
        sg.Text('Рекомендация по затравочному значению', size=(39, 1)),
        sg.Radio(text='', group_id=0, default=True, key='_seed_radio_'),
        sg.InputText(key='_seed_')
    ],
    [
        sg.Text('Рекомендация по списку лайков (через запятую)', size=(39, 1)),
        sg.Radio(text='', group_id=0, key='_liked_radio_'),
        sg.InputText(key='_liked_', default_text='noize mc, лигалайз, guf')
    ],
    [
        sg.Text('Рекомендация по списку дизлайков', size=(39, 1)),
        sg.Radio(text='', group_id=0, key='_disliked_radio_'),
        sg.InputText(key='_disliked_')
    ],
    [
        sg.Text('Сколько артистов выводить (число или "all"):', size=(33, 1)),
        sg.InputText(default_text='5', key='_max_len_', size=(5, 1))
    ],
    [sg.Checkbox('Очищать вывод', default=True, key='_clean_output_')],
    [sg.Button('Очистить поля ввода')],
    [sg.Output(size=(100, 20), key='_output_')],
    [sg.Submit(button_text='Рекомендовать'), sg.Cancel()]
]


def show():
    window = sg.Window('lab3', layout)
    while True:                             # The Event Loop
        event, values = window.read()
        seed = values['_seed_']
        seed_radio = values['_seed_radio_']
        liked = values['_liked_']
        liked_radio = values['_liked_radio_']
        disliked = values['_disliked_']
        disliked_radio = values['_disliked_radio_']
        max_len = 100 if values['_max_len_'].lower() == 'all' else int(values['_max_len_'])
        clean = values['_clean_output_']
        if event in (None, 'Exit', 'Cancel'):
            break
        if event == 'Очистить поля ввода':
            window['_seed_'].Update('')
            window['_liked_'].Update('')
            window['_disliked_'].Update('')
        if event == 'Рекомендовать':
            if seed_radio:
                if clean:
                    window['_output_'].Update('')
                try:
                    interface.recommend_by_seem(seed, max_len)
                except interface.ParseError as e:
                    print('Не могу разобрать аргументы')
                    print(e)
                except interface.ArgumentError as e:
                    print(e)
                except Exception as e:
                    print(f'Неизвестная ошибка: {e}')
            elif liked_radio:
                if clean:
                    window['_output_'].Update('')
                try:
                    interface.recommend_by_liked(liked, max_len)
                except interface.ParseError:
                    print('Не могу разобрать аргументы')
                except interface.ArgumentError as e:
                    print(e)
                except Exception as e:
                    print(f'Неизвестная ошибка: {e}')
            elif disliked_radio:
                if clean:
                    window['_output_'].Update('')
                try:
                    interface.recommend_by_disliked(disliked, max_len)
                except interface.ParseError:
                    print('Не могу разобрать аргументы')
                except Exception as e:
                    print(f'Неизвестная ошибка: {e}')

    window.close()
