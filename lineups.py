#!/usr/bin/python3
#
# Copyright 2023 Big Chungus Open Source, LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# I have no idea what I'm talking about here and am not a lawyer.
# Please play nice and don't roast the code.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is who reads this anyway please go look at
# the program instead if you have time to read this.
# See the License for the specific language governing permissions and
# limitations under the License, I am not a lawyer I am not a lawyer.


"""
Going with a more Data-Oriented Programming style. Not using any strong types (enums, classes)
and purely using strings.

Just gotta make sure the names of players are identifiable enough XD.

Limitations:
* A match will either use a libero for all 3 sets or won't use a libero at all (easy change, but prioritize the other changes)
* Not unit tested, but can be unit tested pretty easily since I made all the functions pure
* No way to compare the strengths of the lineups

Instructions on using this program:
1. Update the definitions under "Team Constraint Definitions" for players that will be in/out.
   If a player is out, their name should NOT appear in *any* of the team constraint definitions
   (remember to update preferences too!).
2. Save the file.
3. Run `python3 lineups.py` on the command line.
"""

from collections import defaultdict
from itertools import combinations
from pprint import pprint

"""
Team Constraint Definitions. This is passed into the main runner produce_match_lineups.
"""
constraints = {
    # Combinations will be generated from here.
    "can_play_setter" : frozenset(["Michelle", "Jasper", "Melissa"]),
    "can_play_outside" : frozenset(["Richard", "Daniel", "Steven", "Tiff"]),
    "can_play_opp" : frozenset(["Chau", "Chris", "Michelle", "Jasper", "Melissa", "Richard", "Tiff"]),
    "can_play_middle" : frozenset(["Steven", "Daniel", "Chris", "Chau", "Jasper"]),
    "can_play_libero" : frozenset(["Bri", "Melissa"]),

    # Not counting libero because this is girls on the court at all times.
    "girls_non_libero" : frozenset(["Michelle", "Tiff", "Melissa"]),

    # These people have huge arms like cannons but not quite like Big Chungus.
    "cannons" : frozenset(["Richard", "Chris"]),

    # Very flexible players may not have a preference.
    "preferences" : {
        "Richard": frozenset(["oh1", "oh2"]),
        "Daniel": frozenset(["oh1", "oh2"]),
        "Chau": frozenset(["opp"]),
        "Jasper": frozenset(["s"]),
        "Michelle": frozenset(["s"]),
        "Tiff": frozenset(["oh1", "oh2"]),
        "Bri": frozenset(["lib"]),
        "Steven": frozenset(["oh1", "oh2"]),
        "Chris": frozenset(["opp"]),
        "Melissa": frozenset(["s"]),
    },

    # Some weeks some players have to take one for the team: that means they don't get to
    # play their preferred position throughout the 3-set match that day. This is needed due
    # to the sheer number of players on the team and the preferred positions people have. I've
    # tried not having this feature and I ended up with 0 possible lineups.
    # 
    # Please update this week by week for everyone to have fair playing time.
    "took_one_for_the_team" : frozenset(["Steven", "Melissa"])
}


"""
Inputs to all these functions can be treated as immutable. Would use a frozendict if it existed w/o
bringing in a dependency.

Functions are pure and only depend on the immutable input.
"""

"""
Applies constraints for a single set (game) within a 3-set match.
"""
def is_lineup_valid(constraints, lineup):
    players = set(lineup.values())
    # No duplicate players in lineup
    if len(players) != len(lineup):
        return False
    # Need firepower cuz we div-4
    if not any(player in players for player in constraints["cannons"]):
        return False
    # Co-ed rules
    if "lib" in lineup:
        players.remove(lineup["lib"])
    if len(players.intersection(constraints["girls_non_libero"])) < 2:
        return False
    return True


"""
Python generator for a lineup for a single set (game) that satisfies is_lineup_valid.
"""
def generate_lineups(constraints):
    has_libero = len(constraints["can_play_libero"]) > 0
    for s in constraints["can_play_setter"]:
        for oh1, oh2 in combinations(constraints["can_play_outside"], 2):
            for mb1, mb2 in combinations(constraints["can_play_middle"], 2):
                for opp in constraints["can_play_opp"]:
                    if has_libero:
                        for lib in constraints["can_play_libero"]:
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
                            


"""
Python generator function for valid lineups.
"""
def generate_valid_lineups(constraints):
    for lineup in generate_lineups(constraints):
        if is_lineup_valid(constraints, lineup):
            yield lineup


"""
Constraints that need to be applied across an entire match (aka 3 sets).

allowed_preferences: a set difference between preferences and took_one_for_the_team.
"""
def constraints_satisfied_for(allowed_preferences, match):
    games_played = defaultdict(int)
    # Leaving as a dict here in case we want to strengthen constraints for a match
    # for playoffs.
    played_preferred_pos = defaultdict(int)
    for lineup in match:
        for pos, player in lineup.items():
            games_played[player] += 1
            if player not in allowed_preferences or pos in allowed_preferences[player]:
                played_preferred_pos[player] += 1
    # Everyone on the team has to play at least 2 sets.
    if any(n < 2 for player, n in games_played.items()):
        return False
    # Everyone (besides those who took_one_for_the_team) has to play their preferred at least
    # once in a set.
    if len(set(allowed_preferences.keys()).difference(set(played_preferred_pos.keys()))) != 0:
        return False
    return True


"""
The sauce.
"""
def produce_match_lineups(constraints):
    n_working_matches = 0
    allowed_preferences = {player:prefs for player, prefs in constraints["preferences"].items() if player not in constraints["took_one_for_the_team"]}
    for match in combinations(generate_valid_lineups(constraints), 3):
        if not constraints_satisfied_for(allowed_preferences, match):
            continue
        print("THIS WORKS")
        n_working_matches += 1
        for lineup in match:
            pprint(lineup)
    print(f"Computed {n_working_matches} lineups that work")


if __name__ == "__main__":
    produce_match_lineups(constraints)
