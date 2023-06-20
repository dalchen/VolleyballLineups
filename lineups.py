#!/usr/bin/python3

from itertools import combinations
from dataclasses import dataclass, fields
from enum import Enum, auto
from pprint import pprint
from typing import Optional
from collections import defaultdict

class Player(Enum):
    Richard = auto()
    Daniel = auto()
    Chau = auto()
    Tiff = auto()
    Jasper = auto()
    Michelle = auto()
    Chris = auto()
    Bri = auto()
    Steven = auto()

can_play_setter = set([Player.Michelle, Player.Jasper])
can_play_outside = set([Player.Richard, Player.Daniel, Player.Steven, Player.Tiff])
can_play_oppo = set([Player.Chau, Player.Chris, Player.Michelle, Player.Jasper, Player.Tiff])
can_play_middle = set([Player.Steven, Player.Daniel, Player.Chris, Player.Chau, Player.Jasper])
can_play_libero = set([Player.Bri])

girls_on_court = set([Player.Michelle, Player.Tiff])

preferences = {
    Player.Richard: set(["oh1", "oh2"]),
    Player.Daniel: set(["oh1", "oh2"]),
    Player.Chau: set(["opp"]),
    Player.Tiff: set(["oh1", "oh2"]),
    Player.Jasper: set(["s"]),
    Player.Michelle: set(["s"]),
    Player.Bri: set(["lib"]),
    Player.Steven: set(["oh1", "oh2"]),
}

valid_lineups = []

for s in can_play_setter:
    for oh1, oh2 in combinations(can_play_outside, 2):
        for mb1, mb2 in combinations(can_play_middle, 2):
            for opp in can_play_oppo:
                for lib in can_play_libero:
                    lineup = {
                        's': s,
                        'oh1': oh1,
                        'oh2': oh2,
                        'mb1': mb1,
                        'mb2': mb2,
                        'opp': opp,
                        'lib': lib
                    }
                    players = set(lineup.values())
                    if len(players) != len(lineup):
                        continue
                    # Need firepower cuz we div-4
                    if Player.Richard not in players or Player.Chris not in players:
                        continue
                    # Co-ed rules
                    if len(players.intersection(girls_on_court)) < 2:
                        continue
                    valid_lineups.append(lineup)


def constraints_satisfied_for(match):
    games_played = defaultdict(int)
    played_preferred_pos = set()
    for lineup in match:
        for pos, player in lineup.items():
            games_played[player] += 1
            if player not in preferences or pos in preferences[player]:
                played_preferred_pos.add(player)
    if any(n < 2 for player, n in games_played.items()):
        return False
    if len(set(preferences.keys()).difference(played_preferred_pos)) != 0:
        return False
    return True

for match in combinations(valid_lineups, 3):
    if not constraints_satisfied_for(match):
        continue
    print("THIS WORKS")
    for lineup in match:
        pprint(lineup)
