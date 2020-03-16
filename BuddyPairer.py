import sys
from random import shuffle

"""
Creates randomised pairings of elements in a list where there are no reciprocal relations (A -> B and B -> A) 
and no self relations (A -> A). Assumes all elements in original input list are unique. Avoids rotation and mirroring
to create pairings, meaning that pairings should be unpredictable.

Available for use under https://opensource.org/licenses/MIT
"""


def create_pairings(buddy_list):
    call_recipients = buddy_list.copy()
    shuffle(call_recipients)
    pairings = dict(zip(buddy_list, call_recipients))
    while not fix(pairings):
        pass
    return pairings


def fix(pairings):
    did_shuffle_self_calls = fix_self_calls(pairings)
    did_shuffle_reciprocals = fix_reciprocal_calls(pairings)
    if not reciprocal_calls(pairings) and not self_calls(pairings):
        return True
    if not (did_shuffle_self_calls and did_shuffle_reciprocals):
        buddy_list = list(pairings.keys())
        call_recipients = buddy_list.copy()
        shuffle(call_recipients)
        new_pairings = dict(zip(buddy_list, call_recipients))
        for buddy in buddy_list:
            pairings[buddy] = new_pairings[buddy]
        return False


def fix_self_calls(pairings):
    return _do_fix(pairings, self_calls)


def fix_reciprocal_calls(pairings):
    return _do_fix(pairings, reciprocal_calls)


def self_calls(pairings):
    return {entry for entry in pairings.items() if pairings[entry[0]] == entry[0]}


def reciprocal_calls(pairings):
    return {
        entry
        for entry in pairings.items()
        if entry[0] == pairings[entry[1]]
        and entry[1] == pairings[entry[0]]
        and not entry[0] == pairings[entry[0]]
    }


def _do_fix(pairings, error_func):
    errors = error_func(pairings)
    # we can't swap over reliably
    if len(errors) <= 1:
        return False
    error_list = list(dict(errors).keys())
    alternatives = list(error_list.copy())
    shuffle(alternatives)
    replacements = zip(error_list, alternatives)
    for replacement in replacements:
        pairings[replacement[0]] = replacement[1]
    return True


if __name__ == "__main__":
    with open(sys.argv[1], "r", encoding="utf-8") as source_file:
        lines = source_file.readlines()
    if len(lines) <= 2:
        print(
            "Can't randomise with <= 2 people - they would always either call themselves or each other"
        )
    lines = [line.strip() for line in lines]
    pairings = create_pairings(lines)
    with open(sys.argv[2], "w") as destination_file:
        destination_file.write("Buddy 1, Buddy2\n")
        for pairing in pairings.items():
            destination_file.write(f"{pairing[0]},{pairing[1]}\n")
