# -*- coding: utf-8 -*-

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

    def get_data(self):
        # Para reemplazar los ids con los tags de los jugadores.
        players_and_ids = [[p['tag'], p['entrant_id']] for p in self.players]
        # Elimina sets con DQs.
        sets = [x for x in self.all_sets if (x['entrant_1_score'] != -1 and x['entrant_2_score'] != -1 and x['bracket_id'] == '499842')]
        # Tomamos los jugadores: J1, J2, ganador.
        # Dividimos entre winners y losers (buscar una forma menos jodidamente horrible de hacerlo, si es posible).
        sets_played_winners = [[item['entrant_1_id'], item['entrant_2_id'], item['winner_id']] for item in sets if "loser" not in item['full_round_text'].lower()]
        sets_played_losers = [[item['entrant_1_id'], item['entrant_2_id'], item['winner_id']] for item in sets if "loser" in item['full_round_text'].lower()]

        # Reordenamos para quedarnos con perdedor-ganador en todos los sets.
        # Lo hacemos en winners y losers.
        for n, _set in enumerate(sets_played_winners):
            sets_played_winners[n] = list(_set[0:2])
            if _set[2] == _set[0]:
                sets_played_winners[n].reverse()

        for n, _set in enumerate(sets_played_losers):
            sets_played_losers[n] = list(_set[0:2])
            if _set[2] == _set[0]:
                sets_played_losers[n].reverse()

        # Sustituímos el id por el tag del jugador.
        # De nuevo en winners y losers.
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

        # Sacamos al archivo.
        f = open("./Data/data_redfox.txt", 'w')
        self.print_data_winners(f, sets_played_winners)
        self.print_data_losers(f, sets_played_losers)
        f.close()


if __name__ == '__main__':

    analyze = Analyzer('redfox-2018-winter-1', 'domingo-smash-4-singles', 'b')
    analyze.get_data()
