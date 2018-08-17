# -*- coding: utf-8 -*-
# DATA EXTRACTOR FOR SMASHGG, USING SMASHGG API.

import pysmash   # Requiere pip install pysmash. Más información: https://github.com/PeterCat12/pysmash
import os
import re

TIER_A_FACTOR = 1.1923064
TIER_B_FACTOR = 1.588010334
TIER_C_FACTOR = 3.535334183

def get_puntuation(points, tier, placement):
    factor = 1
    max_position_points = 49
    if tier == "A":
        factor = TIER_A_FACTOR
        max_position_points = 25
    elif tier == "B":
        factor = TIER_B_FACTOR
        max_position_points = 13
    elif tier == "C":
        factor = TIER_C_FACTOR
        max_position_points = 7

    if placement > max_position_points:
        return 0

    return points / (1000.0 * float(placement) * factor)

# Remove non alphanumeric chars and converts uppercase into lowercase.
def remove_invalid_chars(str):
    pattern = re.compile('[^a-zA-Z0-9áéíóú]+')
    str = str.split("/")[-1].split("|")[-1]
    return pattern.sub('', str.lower())


class Analyzer:
    def __init__(self, tournament, event, tier, points, ids=None):
        self.tournament = tournament
        self.event = event
        self.tier = tier
        self.points = float(points)
        self.ids = ids
        # Wrapper.
        self.smash = pysmash.SmashGG()
        # Datos
        self.players = self.smash.tournament_show_players(self.tournament, self.event)
        self.all_sets = self.smash.tournament_show_sets(self.tournament, self.event)
        # If we specify certain events, select sets from those events.
        if ids:
            self.all_sets = [x for x in self.all_sets if x["bracket_id"] in self.ids]
        # Para imprimir
        self.winners = 'w'
        self.losers = 'l'

    # Sin utilizar
    def print_data_winners(self, file_to_write, sets):
        for current_set in sets:
            # Añade tags eliminando espacios (para operar mejor en el futuro).
            file_to_write.write(' '.join(str(x).replace(' ', '') for x in current_set))
            # Añade tier y salto de línea. La tier debería automatizarse en el futuro, dependiendo del torneo.
            file_to_write.write(' %s %s\n' % (self.tier, self.winners))

    def print_data_losers(self, file_to_write, sets):
        for current_set in sets:
            # Añade tags eliminando espacios (para operar mejor en el futuro).
            file_to_write.write(' '.join(str(x).replace(' ', '') for x in current_set))
            # Añade tier y salto de línea. La tier debería automatizarse en el futuro, dependiendo del torneo.
            file_to_write.write(' %s %s\n' % (self.tier, self.losers))

    # Método de impresión general, sin considerar losers o winners.
    def print_sets(self, file_to_write, sets):
        for current_set in sets:
            # Añade tags eliminando espacios (para operar mejor en el futuro).
            file_to_write.write(' '.join(remove_invalid_chars(str(x)) for x in current_set))
            # Añade tier y salto de línea. La tier debería automatizarse en el futuro, dependiendo del torneo.
            file_to_write.write('\n')

    def print_placement_points(self, file_to_write, placements):
        for element in placements:
            file_to_write.write(remove_invalid_chars(element[0]))
            file_to_write.write(' '+str(get_puntuation(self.points, self.tier, element[1])))
            # Añade salto de línea
            file_to_write.write("\n")

    def get_data(self):
        # Posiciones
        player_placements = [[x["tag"], x["final_placement"]] for x in self.players]
        player_placements.sort(key=lambda x: x[1])

        # Sets
        # Para reemplazar los ids con los tags de los jugadores.
        players_and_ids = [[p['tag'], p['entrant_id']] for p in self.players]
        # Elimina sets con DQs.
        sets = [x for x in self.all_sets if (x['entrant_1_score'] != -1 and x['entrant_2_score'] != -1)]# and x['bracket_id'] == '407328')]
        # Tomamos los jugadores: J1, J2, ganador.
        sets_played = [[item['entrant_1_id'], item['entrant_2_id'], item['winner_id']] for item in sets]
        # División entre winners y losers, no se utiliza (buscar una forma menos jodidamente horrible de hacerlo, si es posible).
        #sets_played_winners = [[item['entrant_1_id'], item['entrant_2_id'], item['winner_id']] for item in sets if "loser" not in item['full_round_text'].lower()]
        #sets_played_losers = [[item['entrant_1_id'], item['entrant_2_id'], item['winner_id']] for item in sets if "loser" in item['full_round_text'].lower()]

        # Reordenamos para quedarnos con ganador-perdedor en todos los sets.
        for n, _set in enumerate(sets_played):
            sets_played[n] = list(_set[0:2])
            if _set[2] == _set[1]:
                sets_played[n].reverse()

        # Sustituímos el id por el tag del jugador.
        for n, _set in enumerate(sets_played):
            for m, player in enumerate(_set):
                for p in players_and_ids:
                    if p[1] == int(player):
                        sets_played[n][m] = p[0]
                        break

        # Sacamos al archivo.
        f = open("./Data2/smashgg_data_{}.txt".format(self.tournament), 'w')
        f.write(self.tournament + "\n")
        f.write(self.tier + "\n")
        #print("Players: {}".format(str(len(player_placements))))
        #print("Sets: {}".format(str(len(sets_played))))
        f.write(str(len(player_placements)) + "\n\n")
        self.print_placement_points(f, player_placements)
        f.write("\n")
        self.print_sets(f, sets_played)
        f.close()


if __name__ == '__main__':
    # Ejemplo
    f = open("./torneossmashgg.txt", 'r')
    for line in f:
        next_tournament = line.split()
        analyze = None
        print(str(next_tournament[0]))
        if len(next_tournament) > 4:
            ids = next_tournament[4].split(",")
            analyze = Analyzer(next_tournament[0], next_tournament[1], next_tournament[2], next_tournament[3], ids)
        else:
            analyze = Analyzer(next_tournament[0], next_tournament[1], next_tournament[2], next_tournament[3])
        analyze.get_data()
