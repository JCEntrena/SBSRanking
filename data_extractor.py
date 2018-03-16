import pysmash
import os, sys

if __name__ == '__main__':

    # Definiciones para trabajo.
    smash = pysmash.SmashGG()

    players = smash.tournament_show_players('redfox-2018-winter-1', 'domingo-smash-4-singles')
    all_sets = smash.tournament_show_sets('redfox-2018-winter-1', 'domingo-smash-4-singles')
    brackets = smash.tournament_show_event_brackets('redfox-2018-winter-1', 'domingo-smash-4-singles')

    # Para reemplazar los ids con los tags de los jugadores.
    players_and_ids = [[p['tag'], p['entrant_id']] for p in players]

    # Elimina sets con DQs.
    sets = [x for x in all_sets if (x['entrant_1_score'] != -1 and x['entrant_2_score'] != -1)]
    # Tomamos los jugadores: J1, J2, ganador.
    sets_played = [[item['entrant_1_id'], item['entrant_2_id'], item['winner_id']] for item in sets]

    #positions = [item['final_placement'] for item in players]

    # Reordenamos para quedarnos con perdedor-ganador en todos los sets.
    for n, _set in enumerate(sets_played):
        sets_played[n] = list(_set[0:2])
        if _set[2] == _set[0]:
            sets_played[n].reverse()

    # Sustituímos el id por el tag del jugador.
    for n, _set in enumerate(sets_played):
        for m, player in enumerate(_set):
            for p in players_and_ids:
                if p[1] == int(player):
                    sets_played[n][m] = p[0]
                    break

    # Escribimos en un archivo.
    f = open("./Data/data_redfox", 'w')

    for current_set in sets_played:
        f.write("%s\n" % current_set)

    f.close()
