# -*- coding: utf-8 -*-
# DATA EXTRACTOR FOR SMASHGG, USING SMASHGG API.

import pysmash   # Requiere pip install pysmash. Más información: https://github.com/PeterCat12/pysmash
import os

class Analyzer:
    def __init__(self, tournament, event, tier):
        self.tournament = tournament
        self.event = event
        self.tier = tier
        # Wrapper.
        self.smash = pysmash.SmashGG()
        # Datos
        self.players = self.smash.tournament_show_players(self.tournament, self.event)
        self.all_sets = self.smash.tournament_show_sets(self.tournament, self.event)
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
            file_to_write.write(' '.join(str(x).replace(' ', '') for x in current_set))
            # Añade tier y salto de línea. La tier debería automatizarse en el futuro, dependiendo del torneo.
            file_to_write.write('\n')

    def print_placements(self, file_to_write, placements):
        for element in placements:
            file_to_write.write(' '.join(str(x).replace(' ', '') for x in element))
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

        # Sacamos al archivo.
        f = open("./Data/data_sal-del-pozo-3", 'w')
        f.write(self.tournament + "\n")
        f.write(self.tier + "\n")
        f.write(str(len(player_placements)) + "\n\n")
        self.print_placements(f, player_placements)
        f.write("\n")
        self.print_sets(f, sets_played)
        f.close()


if __name__ == '__main__':
    # Ejemplo
    analyze = Analyzer('sal-del-pozo-3', 'wii-u-singles', 'c')
    analyze.get_data()
