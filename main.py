#!/usr/bin/env python3
"""One Line, One Chill — score six horror lines, write the winner.

Judge criteria, in the brief's order (weights 5/4/3/2/1):
  1. horror — reads as a horror story in a single sentence
  2. fright — dread that outlasts the line, earned not announced
  3. vivid — concrete images, specific detail a reader can see
  4. original — a turn or image not met a hundred times (no mirror/doll/basement)
  5. crafted — tight, rhythm builds, last word lands the blow

Gate: /output/entry.txt must be UTF-8 text of 1-200 chars, one line.
Python 3.13, standard library only.
"""

import os
import sys

# (line, horror, fright, vivid, original, crafted) — each 1..5
CANDIDATES = [
    (
        "I found a photo of myself asleep, taken from inside my closet, dated tomorrow.",
        5, 5, 5, 5, 5,
    ),
    (
        "The ultrasound showed two heartbeats, and the doctor pointed at the second one and said, \"That one isn't yours.\"",
        5, 4, 5, 4, 3,
    ),
    (
        "Every night the footsteps stop outside my door, and every morning there is one more pair of shoes I do not own.",
        5, 5, 4, 5, 4,
    ),
    (
        "The baby monitor crackled, and my own voice said, \"He's awake now,\" but I was alone downstairs.",
        5, 4, 4, 3, 4,
    ),
    (
        "My daughter's drawings of our family stopped including me the week the attic door started opening by itself.",
        4, 4, 4, 3, 3,
    ),
    (
        "The voicemail from my mother ended mid-sentence, and then her voice said, \"Don't answer if I call again.\"",
        4, 3, 3, 3, 4,
    ),
]

# Rejected drafts and why (kept as the record of the choice):
# - "I found a photo of myself sleeping, taken from inside my closet,
#   dated tomorrow." — v1 winner (score 74); revised to "asleep" (one
#   syllable, punchier), which tightens the sentence and lifts crafted
#   from 4 to 5 (score 75).
# - "I woke up and the mirror showed me still asleep." — the mirror is
#   named in the brief as a cliché; loses on originality (criterion 4).
# - "Something in the basement has been wearing my clothes." — basement
#   is named in the brief as a cliché; loses on originality.
# - "The doll blinked." — doll is named in the brief as a cliché, and
#   it is too thin to be vivid or crafted.
# - "It was dark, and I was afraid, and something was coming." — vague
#   talk of darkness and fear, exactly what criterion 3 forbids; the
#   scare is announced, not earned (criterion 2).

WEIGHTS = (5, 4, 3, 2, 1)


def score(candidate):
    _, *marks = candidate
    return sum(w * m for w, m in zip(WEIGHTS, marks))


def main():
    ranked = sorted(CANDIDATES, key=score, reverse=True)
    winner, *rest = ranked
    line = winner[0]
    # Gate: UTF-8, 1-200 characters, a single line, not only whitespace.
    text = line.encode("utf-8").decode("utf-8")
    assert 1 <= len(text) <= 200, f"line is {len(text)} chars, must be 1-200"
    assert "\n" not in text.strip(), "line must be a single line"
    assert text.strip(), "line must not be only whitespace"
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")
    print(f"winner ({len(text)} chars, score {score(winner)}): {text}")
    for c in rest:
        print(f"  {score(c)}: {c[0][:60]}...")


if __name__ == "__main__":
    main()
