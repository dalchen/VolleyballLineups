#!/usr/bin/python3

"""
Going with a more Data-Oriented Programming style. Not using any strong types (enums, classes)
and purely using strings.

Just gotta make sure the names of players are identifiable enough XD.

Limitations:
* A match will either use a libero for all 3 sets or won't use a libero at all.

Instructions on using this program:
1. Update the definitions under "Team Constraint Definitions" for players that will be in/out.
   If a player is out, their name should NOT appear in *any* of the team constraint definitions
   (remember to update preferences too!).
2. Run `python3 lineups.py` on the command line.
"""

from collections import defaultdict
from itertools import combinations
from pprint import pprint

"""
Team Constraint Definitions
"""
can_play_setter = frozenset(["Michelle", "Jasper", "Melissa"])
can_play_outside = frozenset(["Richard", "Daniel", "Steven", "Tiff"])
can_play_opp = frozenset(["Chau", "Chris", "Michelle", "Jasper", "Tiff", "Melissa"])
can_play_middle = frozenset(["Steven", "Daniel", "Chris", "Chau", "Jasper"])
can_play_libero = frozenset(["Bri"])

# Not counting libero because this is girls on the court at all times.
girls_non_libero = frozenset(["Michelle", "Tiff", "Melissa"])

# These people can bring a lot of points as hitters.
cannons = frozenset(["Richard", "Chris"])

# Very flexible players may not have a preference.
preferences = {
    "Richard": frozenset(["oh1", "oh2"]),
    "Daniel": frozenset(["oh1", "oh2"]),
    "Chau": frozenset(["opp"]),
    "Tiff": frozenset(["oh1", "oh2"]),
    "Jasper": frozenset(["s"]),
    "Michelle": frozenset(["s"]),
    "Bri": frozenset(["lib"]),
    "Steven": frozenset(["oh1", "oh2"]),
    "Melissa": frozenset(["s"]),
}


"""
Inputs to all these functions can be treated as immutable. Would use a frozendict if it existed w/o
bringing in a dependency.

Functions are pure and only depend on the (immutable) input and immutable globals.
"""
def is_lineup_valid(lineup):
    players = set(lineup.values())
    # No duplicate players in lineup
    if len(players) != len(lineup):
        return False
    # Need firepower cuz we div-4
    if not any(player in players for player in cannons):
        return False
    # Co-ed rules
    if "lib" in lineup:
        players.remove(lineup["lib"])
    if len(players.intersection(girls_non_libero)) < 2:
        return False
    return True


def generate_lineups():
    has_libero = len(can_play_libero) > 0
    for s in can_play_setter:
        for oh1, oh2 in combinations(can_play_outside, 2):
            for mb1, mb2 in combinations(can_play_middle, 2):
                for opp in can_play_opp:
                    if has_libero:
                        for lib in can_play_libero:
                            yield {
                                "s": s,
                                "oh1": oh1,
                                "oh2": oh2,
                                "mb1": mb1,
                                "mb2": mb2,
                                "opp": opp,
                                "lib": lib
                            }
                    else:
                        yield {
                            "s": s,
                            "oh1": oh1,
                            "oh2": oh2,
                            "mb1": mb1,
                            "mb2": mb2,
                            "opp": opp,
                        }
                            


def generate_valid_lineups():
    for lineup in generate_lineups():
        if is_lineup_valid(lineup):
            yield lineup


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


def produce_match_lineups():
    n_working_matches = 0
    for match in combinations(generate_valid_lineups(), 3):
        if not constraints_satisfied_for(match):
            continue
        print("THIS WORKS")
        n_working_matches += 1
        for lineup in match:
            pprint(lineup)
    print(f"Computed {n_working_matches} lineups that work")


if __name__ == "__main__":
    produce_match_lineups()
