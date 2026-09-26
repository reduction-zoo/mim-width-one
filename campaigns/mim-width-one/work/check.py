"""Exact finite quartet-consistency and mim-width-one oracles."""

import argparse
import json
import random
import subprocess
import sys
from itertools import combinations
from pathlib import Path


def legal_source(source):
    if not isinstance(source,dict) or set(source) != {"taxa","quartets"}:
        return False
    n,quartets = source["taxa"],source["quartets"]
    return (type(n) is int and n >= 4 and isinstance(quartets,list)
            and all(isinstance(q,list) and len(q) == 4
                    and all(type(v) is int and 0 <= v < n for v in q)
                    and len(set(q)) == 4 and q[0] < q[1] and q[2] < q[3]
                    and q[0] < q[2] for q in quartets)
            and len({tuple(q) for q in quartets}) == len(quartets))


def legal_target(target):
    if not isinstance(target,dict) or set(target) != {"vertices","edges"}:
        return False
    n,edges = target["vertices"],target["edges"]
    return (type(n) is int and n >= 2 and isinstance(edges,list)
            and all(isinstance(edge,list) and len(edge) == 2
                    and all(type(v) is int and 0 <= v < n for v in edge)
                    and edge[0] < edge[1] for edge in edges)
            and len({tuple(edge) for edge in edges}) == len(edges))


def all_trees(n):
    trees = [((0,1),)]
    for leaf in range(2,n):
        internal = n+leaf-2
        following = []
        for edges in trees:
            for old in edges:
                new = [edge for edge in edges if edge != old]
                u,v = old
                new += [(min(u,internal),max(u,internal)),
                        (min(v,internal),max(v,internal)),
                        (leaf,internal)]
                following.append(tuple(sorted(new)))
        trees = following
    return trees


def legal_tree(n,output):
    if not isinstance(output,dict) or set(output) != {"edges"}:
        return False
    edges = output["edges"]
    total = 2*n-2
    if (not isinstance(edges,list) or len(edges) != total-1
            or any(not isinstance(edge,list) or len(edge) != 2
                   or any(type(v) is not int or not 0 <= v < total for v in edge)
                   or edge[0] == edge[1] for edge in edges)):
        return False
    adjacent = [set() for _ in range(total)]
    for u,v in edges:
        adjacent[u].add(v)
        adjacent[v].add(u)
    if any(len(adjacent[v]) != (1 if v < n else 3) for v in range(total)):
        return False
    seen,frontier = {0},[0]
    while frontier:
        for v in adjacent[frontier.pop()]:
            if v not in seen:
                seen.add(v)
                frontier.append(v)
    return len(seen) == total


def tree_splits(n,edges):
    total = 2*n-2
    adjacent = [set() for _ in range(total)]
    for u,v in edges:
        adjacent[u].add(v)
        adjacent[v].add(u)
    splits = []
    for a,b in edges:
        visited,frontier = {a},[a]
        while frontier:
            u = frontier.pop()
            for v in adjacent[u]:
                if (u == a and v == b) or (u == b and v == a):
                    continue
                if v not in visited:
                    visited.add(v)
                    frontier.append(v)
        splits.append({v for v in visited if v < n})
    return splits


def displays(source,edges):
    splits = tree_splits(source["taxa"],edges)
    for a,b,c,d in source["quartets"]:
        if not any((a in side and b in side and c not in side and d not in side)
                   or (c in side and d in side and a not in side and b not in side)
                   for side in splits):
            return False
    return True


def induced_matching_two(target,side):
    edges = {tuple(edge) for edge in target["edges"]}
    crossing = [(u,v) if u in side else (v,u) for u,v in edges if (u in side) != (v in side)]
    for (a,b),(c,d) in combinations(crossing,2):
        if a != c and b != d and tuple(sorted((a,d))) not in edges and tuple(sorted((c,b))) not in edges:
            return True
    return False


def width_one(target,edges):
    return all(not induced_matching_two(target,side)
               for side in tree_splits(target["vertices"],edges))


def source_solutions(source,limit=3):
    if not legal_source(source):
        raise ValueError("Illegal quartet instance")
    outputs = []
    for edges in all_trees(source["taxa"]):
        if displays(source,edges):
            outputs.append({"edges":[list(edge) for edge in edges]})
            if len(outputs) >= limit:
                break
    return outputs or [{"status":"NO-SOLUTION"}]


def target_solutions(target,limit=3):
    if not legal_target(target):
        raise ValueError("Illegal graph")
    outputs = []
    for edges in all_trees(target["vertices"]):
        if width_one(target,edges):
            outputs.append({"edges":[list(edge) for edge in edges]})
            if len(outputs) >= limit:
                break
    return outputs or [{"status":"NO-SOLUTION"}]


def solve_source(source):
    return source_solutions(source,1)[0]


def solve_target(target):
    return target_solutions(target,1)[0]


def valid_source(source,output):
    if not legal_source(source) or not isinstance(output,dict):
        return False
    if output == {"status":"NO-SOLUTION"}:
        return solve_source(source) == output
    return legal_tree(source["taxa"],output) and displays(source,output["edges"])


def valid_target(target,output):
    if not legal_target(target) or not isinstance(output,dict):
        return False
    if output == {"status":"NO-SOLUTION"}:
        return solve_target(target) == output
    return legal_tree(target["vertices"],output) and width_one(target,output["edges"])


def self_test():
    from generate_cases import EDGE_CASES,random_source
    from test_oracle import test_hand_cases
    root = Path(__file__).resolve().parents[3]
    path = Path(__file__).with_name("cases.json")
    subprocess.run([sys.executable,str(root/"research/validate_preparation.py"),str(path)],check=True,cwd=root)
    cases = json.loads(path.read_text())
    assert [len(all_trees(n)) for n in range(2,7)] == [1,1,3,15,105]
    for source,expected in EDGE_CASES:
        assert ("edges" in solve_source(source)) == expected
    for case in cases:
        source = case["source"]
        if case["kind"] == "random":
            assert random_source(case["seed"]) == source
        current = solve_source(source)
        assert ("edges" in current) == ("edges" in case["expected"])
        assert valid_source(source,current) and valid_source(source,case["expected"])
    test_hand_cases()
    yes,no = 0,0
    for seed in range(100):
        rng = random.Random(seed)
        n = rng.randint(2,6)
        target = {"vertices":n,"edges":[[u,v] for u in range(n) for v in range(u+1,n)
                                            if rng.randrange(2)]}
        answer = solve_target(target)
        assert valid_target(target,answer)
        yes += "edges" in answer
        no += "edges" not in answer
    print(f"Self-test passed: {len(cases)} quartet cases and {yes} YES/{no} NO target graphs")


def candidate_check(path):
    self_test()
    cases = json.loads(Path(__file__).with_name("cases.json").read_text())
    recovered = 0
    for case in cases:
        source = case["source"]
        forward = subprocess.run([sys.executable,str(path)],input=json.dumps(source),text=True,capture_output=True,check=True)
        target = json.loads(forward.stdout)
        if not legal_target(target):
            raise AssertionError(f"Illegal target: {target}")
        for output in target_solutions(target):
            assert valid_target(target,output)
            payload = {"source":source,"target_solution":output}
            extraction = subprocess.run([sys.executable,str(path),"--extract"],input=json.dumps(payload),text=True,capture_output=True,check=True)
            recovered_output = json.loads(extraction.stdout)
            if not valid_source(source,recovered_output):
                raise AssertionError(f"Invalid recovery from {output}: {recovered_output}")
            recovered += 1
    print(f"Candidate check passed: {len(cases)} source cases, {recovered} target outputs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test",action="store_true")
    group.add_argument("--candidate",type=Path)
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        candidate_check(args.candidate)
