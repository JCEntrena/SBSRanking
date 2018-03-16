# -*- coding: utf-8 -*-

import pysmash   # Requiere pip install pysmash. Más información: https://github.com/PeterCat12/pysmash
import os

if __name__ == '__main__':

    # Definiciones para trabajo.
    smash = pysmash.SmashGG()

    players = smash.tournament_show_players('redfox-2018-winter-1', 'domingo-smash-4-singles')
    all_sets = smash.tournament_show_sets('redfox-2018-winter-1', 'domingo-smash-4-singles')

    # Para reemplazar los ids con los tags de los jugadores.
    players_and_ids = [[p['tag'], p['entrant_id']] for p in players]

    # Elimina sets con DQs.
    sets = [x for x in all_sets if (x['entrant_1_score'] != -1 and x['entrant_2_score'] != -1 and x['bracket_id'] == '499842')]
    # Tomamos los jugadores: J1, J2, ganador
    sets_played_winners = [[item['entrant_1_id'], item['entrant_2_id'], item['winner_id']] for item in sets if "loser" not in item['full_round_text'].lower()]
    sets_played_losers = [[item['entrant_1_id'], item['entrant_2_id'], item['winner_id']] for item in sets if "loser" in item['full_round_text'].lower()]

    #positions = [item['final_placement'] for item in players]

    # Reordenamos para quedarnos con perdedor-ganador en todos los sets.
    for n, _set in enumerate(sets_played_winners):
        sets_played_winners[n] = list(_set[0:2])
        if _set[2] == _set[0]:
            sets_played_winners[n].reverse()

    for n, _set in enumerate(sets_played_losers):
        sets_played_losers[n] = list(_set[0:2])
        if _set[2] == _set[0]:
            sets_played_losers[n].reverse()

    # Sustituímos el id por el tag del jugador.
    for n, _set in enumerate(sets_played_winners):
        for m, player in enumerate(_set):
            for p in players_and_ids:
                if p[1] == int(player):
                    sets_played_winners[n][m] = p[0]
                    break

    for n, _set in enumerate(sets_played_losers):
        for m, player in enumerate(_set):
            for p in players_and_ids:
                if p[1] == int(player):
                    sets_played_losers[n][m] = p[0]
                    break

    # Escribimos en un archivo.
    f = open("./Data/data_redfox", 'w')

    for current_set in sets_played_winners:
        # Añade tags eliminando espacios (para operar mejor en el futuro).
        f.write(' '.join(str(x).replace(' ', '') for x in current_set))
        # Añade tier y salto de línea. La tier debería automatizarse en el futuro, dependiendo del torneo.
        f.write(' B W\n')

    for current_set in sets_played_losers:
        # Añade tags eliminando espacios (para operar mejor en el futuro).
        f.write(' '.join(str(x).replace(' ', '') for x in current_set))
        # Añade tier y salto de línea. La tier debería automatizarse en el futuro, dependiendo del torneo.
        f.write(' B L\n')

    f.close()
