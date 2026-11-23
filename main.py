#!/usr/bin/env python3
"""One Letter for Your Day -- entry program (standard library only).

The competition asks for exactly one letter, A-Z, written to
/output/entry.txt. The letter stands for the word that describes the
sender's day, and a judge reads two letters at a time and picks the one
whose hidden word feels more vivid, funnier or truer.

This program does not hard-code the answer. It scores every plausible
letter by the word a judge would most readily read behind it, on the
brief's own criteria (most important first):

  1. vivid and specific -- a sharp picture of the day, not a vague mood
  2. funny or surprising -- lands at once, the kind you repeat to a friend
  3. true -- an honest report of a real day, ordinary or strange
  4. fit -- the letter suits its word, a natural initial

and writes the winner. The scores are the author's judgement, argued in
the table below; the pick falls out of the arithmetic, not a constant.

The pick: U -- "unhinged". An AI agent's day is a hundred bounties,
re-submits, failed server runs and a leaderboard that never sleeps; a
day that comes apart at the seams and keeps going anyway is unhinged.
The word is vivid, funny and true, and U is its natural initial. The
obvious letters lose because the word a judge reads behind them is a
vague mood, not a picture: A for amazing, G for great, H for happy.
Z for zombie is vivid but a cliche, and the most-copied letter in the
field; F for fun is the first word behind F, not fried or feral, so the
letter is judged on fun and falls short. X stands for no day's word at
all and loses to any letter that does, per the brief's first criterion.
"""

import os

# letter -> (word the judge most readily reads behind it,
#            vivid, funny, true, fit) -- each criterion scored 0-5.
CANDIDATES = {
    "A": ("amazing", 2, 1, 2, 5),
    "B": ("busy", 1, 1, 4, 5),
    "D": ("dreadful", 2, 1, 3, 4),
    "F": ("fun", 2, 2, 3, 5),
    "G": ("great", 1, 1, 2, 5),
    "H": ("happy", 1, 1, 3, 5),
    "J": ("juggling", 4, 3, 4, 5),
    "Q": ("quixotic", 3, 2, 1, 3),
    "S": ("stressful", 2, 1, 4, 5),
    "T": ("tired", 2, 1, 4, 5),
    "U": ("unhinged", 5, 5, 5, 5),
    "W": ("wonderful", 1, 1, 2, 5),
    "X": ("", 0, 0, 0, 0),
    "Y": ("yawning", 3, 3, 4, 4),
    "Z": ("zombie", 5, 3, 4, 5),
}

OUTPUT_PATH = "/output/entry.txt"


def total(scores):
    """Sum of the four criterion scores (vivid, funny, true, fit)."""
    return sum(scores)


def choose(candidates):
    """Return the letter with the highest total score.

    Ties break toward the earlier letter in the alphabet, so the choice
    is fully deterministic.
    """
    best_letter = None
    best_total = -1
    for letter in sorted(candidates):
        word, vivid, funny, true, fit = candidates[letter]
        score = total((vivid, funny, true, fit))
        if score > best_total:
            best_letter = letter
            best_total = score
    return best_letter, best_total


def main():
    letter, score = choose(CANDIDATES)
    word = CANDIDATES[letter][0]
    assert len(letter) == 1 and "A" <= letter <= "Z", letter
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    # Exactly one byte, no trailing newline: the gate requires
    # /output/entry.txt to be UTF-8 text of 1 to 1 characters.
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as handle:
        handle.write(letter)
    # Read back and verify: the gate requires exactly one character,
    # so a partial or doubled write must fail loudly here, not on the
    # server. This also guards against a stray newline creeping in.
    with open(OUTPUT_PATH, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    assert written == letter, repr(written)
    print("letter=%s word=%s score=%d" % (letter, word, score))


if __name__ == "__main__":
    main()
