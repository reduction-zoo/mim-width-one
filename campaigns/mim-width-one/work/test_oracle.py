from check import legal_source,solve_source,valid_source,legal_target,solve_target,valid_target


def test_hand_cases():
    quartet = {"taxa":4,"quartets":[[0,1,2,3]]}
    tree = {"edges":[[0,4],[1,4],[4,5],[2,5],[3,5]]}
    assert valid_source(quartet,tree)
    conflict = {"taxa":4,"quartets":[[0,1,2,3],[0,2,1,3]]}
    assert solve_source(conflict) == {"status":"NO-SOLUTION"}
    assert not legal_source({"taxa":4,"quartets":[[0,0,1,2]]})
    empty = {"vertices":4,"edges":[]}
    assert valid_target(empty,tree)
    assert not legal_target({"vertices":3,"edges":[[1,0]]})
    hard = {"vertices":6,"edges":[[0,2],[0,3],[1,3],[1,4],[1,5],[2,4],[2,5],[3,5]]}
    assert solve_target(hard) == {"status":"NO-SOLUTION"}


if __name__ == "__main__":
    test_hand_cases()
