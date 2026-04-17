import FreeSimpleGUI as sg


def display_ini ():
    button_size = (7, 3)
    deck = [0, 0, 0,
            0, 0, 0,
            0, 0, 0]

    widget = [  [sg.Button("", key = '-0-', size = button_size),
                 sg.Button("", key = '-1-', size = button_size),
                 sg.Button("", key = '-2-',size = button_size)],

                [sg.Button("", key = '-3-', size = button_size),
                 sg.Button("", key = '-4-', size = button_size),
                 sg.Button("", key = '-5-',size = button_size)],

                [sg.Button("", key = '-6-', size = button_size),
                 sg.Button("", key = '-7-', size = button_size),
                 sg.Button("", key = '-8-', size = button_size)],
                [sg.Text('', key = '-WINNER-')],
                [sg.Button('Finalizar', key = '-OK-'), sg.Button('Reiniciar', key = '-CLEAN-')]   ]
    return deck ,widget


def main ():
    deck, widget = display_ini()
    window = sg.Window('Demo', widget) #.read() 'inicia visualizacion' # Window('Demo', [[]], margins =(100, 100)) >se llama: windows(widget)
    PLAYER_ONE = 'X'
    PLAYER_TWO = 'O'
    current_player = PLAYER_ONE
    winner_plays = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    game_end = False

    while True:
        event, value = window.read()
        #print(event, value)
        if event == sg.WIN_CLOSED or event == '-OK-':
            break
        elif event == '-CLEAN-':
            deck, widget = display_ini()
            for button in range(9):
                window.Element(f'-{button}-').Update('')
            current_player = PLAYER_ONE
            game_end = False
            window.Element('-WINNER-').Update(value='')

        if window.Element(event).ButtonText == '' and not game_end:
            indice = int(event.replace('-', ''))
            deck[indice] = current_player
            window.Element(event).Update(text = current_player)
            #print(deck)

            for winner_play in winner_plays:
                if deck[winner_play[0]] == deck[winner_play[1]] == deck[winner_play[2]] != 0:
                    if deck[winner_play[0]] == PLAYER_ONE:
                        print('\x1b[3m\x1b[31mEl jugador 1 ha ganado!!!\x1b[0m')
                        window.Element('-WINNER-').Update(value = 'El jugador 1 haganado!!')
                        sg.popup('P1 WINS',title = 'Fin')
                    else:
                        print('\x1b[3m\x1b[34mEl jugador 2 ha ganado!!!\x1b[0m')
                        window.Element('-WINNER-').Update(value='El jugador 2 haganado!!')
                        sg.popup('P2 WINS', title='Fin')
                    game_end = True

            if 0 not in deck:
                print('Juego terminado!')
                window.Element('-WINNER-').Update(value='Juego terminado')
                game_end = True

            if current_player == PLAYER_ONE:
                current_player = PLAYER_TWO
            else:
                current_player = PLAYER_ONE

    window.close()


if __name__ == '__main__':
    main()