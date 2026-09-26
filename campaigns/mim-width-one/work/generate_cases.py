"""Fix reproducible quartet-consistency cases."""

import json
import random
from itertools import combinations
from pathlib import Path


def quartet(a,b,c,d):
    left,right = sorted((a,b)),sorted((c,d))
    if left[0] > right[0]:
        left,right = right,left
    return left+right


def source(n,quartets):
    return {"taxa":n,"quartets":sorted(quartets)}


EDGE_CASES = [
    (source(4,[]),True),
    (source(4,[[0,1,2,3]]),True),
    (source(4,[[0,2,1,3]]),True),
    (source(4,[[0,3,1,2]]),True),
    (source(4,[[0,1,2,3],[0,2,1,3]]),False),
    (source(4,[[0,1,2,3],[0,3,1,2]]),False),
    (source(4,[[0,2,1,3],[0,3,1,2]]),False),
    (source(5,[]),True),
    (source(5,[[0,1,2,3]]),True),
    (source(5,[[0,1,2,3],[0,2,1,3]]),False),
    (source(6,[[0,1,2,3],[0,1,4,5]]),True),
    (source(6,[[0,1,2,3],[0,2,1,3],[0,1,4,5]]),False),
]


def random_source(seed):
    from check import all_trees,displays
    rng = random.Random(seed)
    n = rng.randint(4,6)
    taxa = list(range(n))
    if seed % 2:
        four = rng.sample(taxa,4)
        a,b,c,d = four
        quartets = [quartet(a,b,c,d),quartet(a,c,b,d)]
        for _ in range(rng.randint(0,3)):
            a,b,c,d = rng.sample(taxa,4)
            q = quartet(a,b,c,d)
            if q not in quartets:
                quartets.append(q)
        return source(n,quartets)
    tree = rng.choice(all_trees(n))
    quartets = []
    for a,b,c,d in combinations(taxa,4):
        for q in (quartet(a,b,c,d),quartet(a,c,b,d),quartet(a,d,b,c)):
            if displays(source(n,[q]),tree) and rng.randrange(2):
                quartets.append(q)
    return source(n,quartets)


def build_cases():
    from check import solve_source
    cases,seen = [],set()

    def add(instance,kind,seed=None,expected=None):
        key = json.dumps(instance,sort_keys=True,separators=(",",":"))
        if key in seen:
            return False
        answer = solve_source(instance)
        if expected is not None and ("edges" in answer) != expected:
            raise AssertionError(f"Hand label disagrees with oracle: {instance}")
        seen.add(key)
        case = {"source":instance,"kind":kind,"expected":answer}
        if seed is not None:
            case["seed"] = seed
        cases.append(case)
        return True

    for instance,expected in EDGE_CASES:
        add(instance,"edge",expected=expected)
    seed = 0
    while sum(case["kind"] == "random" for case in cases) < 100:
        add(random_source(seed),"random",seed=seed)
        seed += 1
    return cases


if __name__ == "__main__":
    path = Path(__file__).with_name("cases.json")
    cases = build_cases()
    path.write_text(json.dumps(cases,indent=2)+"\n")
    print(f"Wrote {len(cases)} cases to {path}")
