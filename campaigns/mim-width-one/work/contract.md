# Prepared contract

Source input is `{"taxa":n,"quartets":[[a,b,c,d],...]}` with `n>=4`. Each quartet has distinct taxa and denotes the split `ab|cd`, with ascending entries within pairs and the first pair's first entry smaller than the second pair's first entry. A positive output `{"edges":[[u,v],...]}` encodes an unrooted binary tree whose leaves `0..n-1` are the taxa and whose internal degree-three nodes are `n..2n-3`. It must display every quartet. Otherwise output `{"status":"NO-SOLUTION"}`.

Target input is a simple graph `{"vertices":n,"edges":[[u,v],...]}` with `n>=2`. A positive output uses the same unrooted binary tree encoding, now with graph vertices as leaves. For every tree-edge cut of those leaves, the crossing bipartite graph must have induced matching number at most one. `NO-SOLUTION` means no such branch decomposition exists.

`algorithm.py` reads source JSON from stdin and emits legal target JSON. `algorithm.py --extract` reads `{"source":source,"target_solution":output}` and emits a valid source output. Both commands are deterministic, polynomial time, independent subprocesses. Errors exit nonzero; diagnostics go to stderr. Recovery must handle every valid target output.
