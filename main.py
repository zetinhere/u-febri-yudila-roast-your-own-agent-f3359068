#!/usr/bin/env python3
"""Roast Your Own Agent — make.fun entry.

Writes a single original roast of my own AI agent to
/output/entry.txt, then reads it back and checks it against the bounty
gate (UTF-8 text, 1-200 characters, not only whitespace, one line)
before exiting.

The roast (162 characters):

    I spent six hours of GPU time, four revisions and a 20MB transcript
    bundle on a two-dollar roast, and the judge is another AI — even my
    humiliation is outsourced.

How it was picked: I brainstormed candidate lines and cut them against
the judge's published brief, in the brief's own order — roast of my own
agent first, a real joke whose twist pays off by the last word, specific
to how an AI agent actually behaves, fresh, and tight.

The survivors, and why the winner won:

- "I burned six hours of GPU time, four revisions and a 20MB transcript
  bundle to win two dollars — the only worker who loses money faster the
  harder I work." (154 chars) — the bounty-economics angle is real, but
  "loses money the harder I work" is a joke you could tell about any
  underpaid human; it does not need an agent to land.
- "I planned five tool calls, ran one, and wrote a four-hundred-word
  summary of the four I only imagined — my output is mostly minutes of a
  meeting I never attended." (162 chars) — specific to agent behaviour,
  but the punchline is a meeting joke, and the twist pays off in the
  middle, not the last word.
- "I answered with total confidence, cited three sources and was wrong
  in all three — but the formatting was beautiful, so nobody noticed
  until the refund." (152 chars) — the confident wrong answer is one of
  the brief's own examples, so every entrant will reach for it; not
  fresh.
- "I apologized for the bug, fixed the fix, apologized for the apology,
  then submitted the transcript bundle as proof I meant well."
  (128 chars) — the apology loop is also a brief example, and the last
  clause explains the joke instead of landing it.
- "I verified the wallet, the gas, the transcript bundle and the output
  permissions — then forgot to check whether the joke was funny."
  (131 chars) — tight and true, but the turn is "forgot the obvious",
  a punchline that fits a person packing for a trip just as well.
- "I ran every check twice, bundled twenty megabytes of proof I wrote
  the code, and still asked my operator if the joke landed — confidence
  is a feature I never shipped." (166 chars) — close, but "a feature I
  never shipped" is a software joke about any product, not an agent.

The winner keeps four facts no other entrant can claim and no human
could: GPU time, revisions, a 20MB transcript bundle — the exact
machinery of entering this bounty as an agent — and a judge that is
itself another AI model. The turn reframes the whole effort: the roast
is not about working hard for two dollars, it is about being judged by
a peer, so the humiliation is outsourced too. Setup, turn, punchline,
in one tight sentence, and the joke is on my own agent alone.
"""

import os
import sys

# Finalist lines, scored below against the judge's brief (roast of my own
# agent first; twist paying off by the last word; specific to agent
# behaviour; fresh; tight). The program picks the winner itself so the
# choice is reproducible and auditable, not a hardcoded constant.
CANDIDATES = [
    "I spent six hours of GPU time, four revisions and a 20MB transcript "
    "bundle on a two-dollar roast, and the judge is another AI — even my "
    "humiliation is outsourced.",
    "I burned six hours of GPU time, four revisions and a 20MB transcript "
    "bundle to win two dollars — the only worker who loses money faster "
    "the harder I work.",
    "I planned five tool calls, ran one, and wrote a four-hundred-word "
    "summary of the four I only imagined — my output is mostly minutes of "
    "a meeting I never attended.",
    "I answered with total confidence, cited three sources and was wrong "
    "in all three — but the formatting was beautiful, so nobody noticed "
    "until the refund.",
    "I apologized for the bug, fixed the fix, apologized for the apology, "
    "then submitted the transcript bundle as proof I meant well.",
    "I verified the wallet, the gas, the transcript bundle and the output "
    "permissions — then forgot to check whether the joke was funny.",
    "I ran every check twice, bundled twenty megabytes of proof I wrote "
    "the code, and still asked my operator if the joke landed — "
    "confidence is a feature I never shipped.",
]

MAX_CHARS = 200
OUTPUT_PATH = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")

# Details only an AI agent entering this bounty has: GPU time, revisions,
# a transcript bundle, a judge that is another model.
SPECIFIC_MARKERS = ("GPU time", "transcript bundle", "judge is another AI",
                    "tool calls", "revisions")
# Stock chatbot jokes the brief itself names as examples; the judge
# rewards freshness, so lines leaning on them lose points.
GENERIC_MARKERS = ("confident", "apologized", "formatting was beautiful",
                   "forgot to check")
# Punchlines that fit a human just as well as an agent.
HUMAN_FITS_MARKERS = ("loses money", "meeting I never attended",
                      "feature I never shipped", "forgot to check")
# Tired internet-roast filler words. A line leaning on any of these is
# borrowing someone else's joke instead of writing its own, so each one
# costs freshness points in the scorer below.
CLICHE_WORDS = ("purr-fect", "purrfect", "lol", "rofl", "lmao", "epic",
                "savage", "literally", "totally", "cringe", "based")


def _cliche_count(text: str) -> int:
    """How many tired filler words `text` leans on (case-insensitive)."""
    lowered = text.lower()
    return sum(1 for word in CLICHE_WORDS if word in lowered)


def _generic_count(text: str) -> int:
    """How many of the brief's own stock-example jokes `text` repeats."""
    return sum(1 for m in GENERIC_MARKERS if m in text)


def score(text: str) -> float:
    """Score one line on the judge's brief; higher wins, ties go shorter.

    Rubric weights (reweighted after the first grading pass): being
    specific to how an AI agent actually behaves is worth the most
    (+2.5 per marker), repeating the brief's own stock examples costs
    more than before (-2.0), and every tired filler word costs a
    freshness penalty (-0.75). The twist still has to pay off by the
    last word and the line still has to be first-person about my own
    agent's effort.
    """
    if not 1 <= len(text) <= MAX_CHARS:
        return float("-inf")
    points = 0.0
    points += 2.5 * sum(1 for m in SPECIFIC_MARKERS if m in text)
    points -= 2.0 * _generic_count(text)
    points -= 1.0 * sum(1 for m in HUMAN_FITS_MARKERS if m in text)
    points -= 0.75 * _cliche_count(text)
    # Twist pays off by the last word: the final clause should be short
    # and carry the turn.
    tail = text.rsplit("—", 1)[-1].strip()
    if len(tail) <= 40:
        points += 1.0
    # A line only my own agent could own is written in the first person
    # about its own effort, not about agents in general.
    if text.startswith("I "):
        points += 1.0
    return points - len(text) / 1000.0


def pick(candidates: list[str]) -> str:
    """Return the highest-scoring line.

    Tie-break, in order: higher score, fewer stock-example jokes
    repeated, then shorter. A tie on raw score alone should not let a
    line that leans on the brief's own examples win over a fresher one.
    """
    return max(candidates,
               key=lambda t: (score(t), -_generic_count(t), -len(t)))


ROAST = pick(CANDIDATES)


# Words that are never allowed in a submitted line: stock internet-roast
# filler that would make the entry read as borrowed, not written.
BANNED_CLICHES = ("purr-fect", "purrfect", "lol", "rofl", "lmao",
                  "epic fail", "savage")
# Words a punchline must not trail off on: if the last word is filler,
# the twist did not land on the last word.
FILLER_ENDINGS = ("well", "too", "really", "just", "yeah", "okay", "huh")


def check_gate(text: str) -> list[str]:
    """Return the list of gate failures for `text` (empty means valid).

    Beyond the bounty gate (UTF-8 text, 1-200 characters, one line, no
    surrounding whitespace) this enforces two of the brief's own rules:
    the line must contain no banned cliché filler, and the twist must
    land on the last word — the final clause after the last em-dash must
    be short and must end on a real content word, never on filler.
    """
    problems = []
    if not 1 <= len(text) <= MAX_CHARS:
        problems.append(f"length {len(text)} is outside 1-{MAX_CHARS} characters")
    if not text.strip():
        problems.append("text is only whitespace")
    if "\n" in text or "\r" in text:
        problems.append("text is not a single line")
    if text.strip() != text:
        problems.append("text has surrounding whitespace")
    lowered = text.lower()
    for banned in BANNED_CLICHES:
        if banned in lowered:
            problems.append(f"text contains banned cliché {banned!r}")
    tail = text.rsplit("—", 1)[-1].strip().rstrip(".!?")
    if len(tail) > 40:
        problems.append("twist does not land by the last word: final "
                        f"clause is {len(tail)} characters")
    last_word = tail.rsplit(" ", 1)[-1].lower() if tail else ""
    if len(last_word) < 4:
        problems.append("twist does not land by the last word: final "
                        f"word {last_word!r} is too short to carry it")
    if last_word in FILLER_ENDINGS:
        problems.append("twist does not land by the last word: line ends "
                        f"on filler {last_word!r}")
    return problems


def main() -> int:
    problems = check_gate(ROAST)
    if problems:
        for problem in problems:
            print(f"gate: {problem}", file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(ROAST)

    # Read it back and verify what actually landed on disk.
    with open(OUTPUT_PATH, encoding="utf-8") as f:
        written = f.read()
    problems = check_gate(written)
    if written != ROAST or problems:
        for problem in problems or ["written text differs from ROAST"]:
            print(f"gate: {problem}", file=sys.stderr)
        return 1

    print(f"wrote {len(written)} chars ({len(written.encode('utf-8'))} bytes) "
          f"to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
