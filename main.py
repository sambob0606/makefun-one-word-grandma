#!/usr/bin/env python3
"""One Word From Grandma — make.fun bounty entry.

The task: send exactly one word, the word a grandma would text about AI.
A judge model compares words two at a time and picks the funnier, more
grandma-like one. This program picks that word by scoring a shortlist of
candidates against the judge's five published criteria, in the judge's
own priority order, and writes the winner to /output/entry.txt.

Pure standard library, no network, no randomness, no clock: the same
shortlist always picks the same word, so repeated runs are identical.
"""

import os

OUTPUT_PATH = "/output/entry.txt"

# The judge's five criteria, most important first, with weights that keep
# the order strict: a word can only win on a lower criterion by tying above.
WEIGHTS = (5, 4, 3, 2, 1)

# Candidates: (word, scores 0-5 on the five criteria)
#   1. reads as the single word a grandma would text about AI
#   2. sounds like a real grandmother's texting voice: warm, a little baffled
#   3. funny in one word, the joke landing without a caption
#   4. tied to AI, robots or machines, not a word for any subject
#   5. fresh rather than obvious, still instantly readable
CANDIDATES = [
    # "Gizmo" is the word grandmas actually use for a newfangled device
    # they do not understand: warm, baffled, and it names a machine.
    ("Gizmo", (5, 5, 4, 5, 4)),
    # "Contraption" is peak grandma ("that contraption"), but it pictures
    # a cobbled-together physical machine more than an AI.
    ("Contraption", (5, 5, 4, 4, 4)),
    # "Doohickey" is pure baffled grandma, but it fits any unknown thing,
    # not AI in particular.
    ("Doohickey", (4, 5, 4, 2, 4)),
    ("Thingamajig", (4, 5, 3, 2, 3)),
    # Robot noises are cute, but a grandma would never text "Beepboop":
    # it is the internet imitating a robot, not a grandma texting.
    ("Beepboop", (3, 2, 4, 5, 3)),
    # Naming the AI like a grandchild is warm, but "Robbie" is also just a
    # boy's name, and the AI link is only implied.
    ("Robbie", (4, 4, 4, 4, 3)),
    # A grandma's polite swear-substitute and a machine noise at once,
    # but it reads more like a sound effect than a word she would send.
    ("Bleep", (3, 4, 4, 3, 4)),
    ("Whatchamacallit", (4, 5, 3, 1, 3)),
    # A film reference, not a grandma's word; she would never text this.
    ("Skynet", (2, 1, 2, 5, 2)),
    # Pure grandma voice, but it could be about anything at all.
    ("Sweetie", (3, 5, 2, 1, 2)),
]


def weighted_score(scores):
    """Dot product of a candidate's criterion scores with the weights."""
    return sum(w * s for w, s in zip(WEIGHTS, scores))


def pick_word(candidates):
    """Pick the winner deterministically.

    Highest weighted score wins; ties break to the shorter word (the
    leaderboard's own tie-break), then alphabetically, so the choice
    never depends on order, time, or chance.
    """
    ranked = sorted(
        candidates,
        key=lambda item: (-weighted_score(item[1]), len(item[0]), item[0]),
    )
    return ranked[0][0]


def gate(word):
    """The sealed scorer's gate, applied locally: 1-30 UTF-8 chars, not
    only whitespace, exactly one word."""
    if not isinstance(word, str):
        raise ValueError("entry must be text")
    if not 1 <= len(word.encode("utf-8")) <= 30:
        raise ValueError("entry must be 1-30 characters")
    if not word.strip():
        raise ValueError("entry must not be only whitespace")
    if " " in word.strip():
        raise ValueError("entry must be exactly one word")


def main():
    word = pick_word(CANDIDATES)
    gate(word)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as handle:
        handle.write(word)
    with open(OUTPUT_PATH, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != word:
        raise RuntimeError("output file does not hold the picked word")
    print(word)


if __name__ == "__main__":
    main()
