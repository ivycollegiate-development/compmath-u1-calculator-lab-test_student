"""Generate YOUR personalized edge-case set for U1 L13.

Run:  python3 gen_probes.py <your seat number>

Writes `edge_case_probes.py` — a list of edge cases chosen from a seed that
comes from YOUR seat number, so no two students get the same set.

`edge_case_probes.py` is in .gitignore. Do not commit it and do not share it —
the point is that nobody knows your cases in advance.
"""

import random
import sys

# Each group is a category of edge case worth checking in a calculator.
# We shuffle the candidates and hand you a few from each, so every student
# gets a genuinely different set to work through.
POOL = {
    "WRONG_TYPE": [
        "hello", "", "   ", "3.5.1", "1,000", "ten", "--5", "1 2",
        "3 + 4", "NaN", "None", "0x1F", "١٢٣",
    ],
    "HUGE": [
        "1e16", "1e18", "1e300", "1e308", "123456789012345678901234567890",
        "1e-300", "10**16", "99999999999999999999",
    ],
    "BOUNDARY": [
        "0", "-0", "1", "-1", "0.0", "-0.0", "1e-320", "5e-324",
        "-273.15", "-273.16", "-459.67", "-459.68", "273.15", "273.16",
    ],
    "DIV_ZERO": [
        "0", "-0", "0.0", "-0.0", "1e-320", "-1e-320", "0.0000000000000000001",
    ],
}

GROUP_NAMES = list(POOL)
TAKE_PER_GROUP = 3


def build(seed):
    rng = random.Random(seed)
    groups = {}
    for name in GROUP_NAMES:
        picks = rng.sample(POOL[name], TAKE_PER_GROUP)
        groups[name] = picks
    return groups


HEADER = '''"""Your personalized edge cases for U1 L13 — GENERATED, DO NOT COMMIT.

Written by gen_probes.py. This file is in .gitignore on purpose.

Work through each group. For every case write down:
  the input | what actually happened | bug, or correct behavior?

"Correct behavior" is a real and valuable answer. Say so when you find one.
"""

PROBES = {
'''


def render(groups):
    out = [HEADER]
    for name in GROUP_NAMES:
        out.append(f'    "{name}": [\n')
        for probe in groups[name]:
            out.append(f'        {probe!r},\n')
        out.append('    ],\n')
    out.append('}\n')
    out.append('\n# Groups worth working through, in this order:\n')
    out.append(f'GROUPS = {GROUP_NAMES!r}\n')
    return ''.join(out)


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 gen_probes.py <your seat number>")
        print("Example: python3 gen_probes.py 7")
        return 1

    raw = sys.argv[1]
    try:
        seat = int(raw)
    except ValueError:
        print(f"'{raw}' is not a number. Your seat number is a whole number, like 7.")
        return 1

    groups = build(seat)
    with open("edge_case_probes.py", "w") as f:
        f.write(render(groups))

    total = sum(len(v) for v in groups.values())
    print(f"Wrote edge_case_probes.py — {total} cases across {len(GROUP_NAMES)} groups.")
    print("Groups: " + ", ".join(GROUP_NAMES))
    print()
    print("Do NOT commit edge_case_probes.py — it is already in your .gitignore.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
