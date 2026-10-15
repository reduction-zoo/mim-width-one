# mim-width-one

Standalone formal definition of Q023. `record.json` preserves the exact
board source, target, requested result and equation used for this definition.
`Challenge.lean` imports only Mathlib. `Solution.lean` is its identical starting
copy, with the open theorem deliberately unproved.

## Modelling choices

Taxa have an explicit finite label universe; each quartet has four distinct labels. Tree leaves correspond bijectively to that universe. Source trees need not be binary and may contain degree-two subdivisions. Display is the existence of an edge separating the two prescribed pairs. Target decomposition trees are subcubic; degree-two subdivisions are harmless. The bipartite cut graph discards all edges inside either side before computing induced matching number. Empty and singleton label sets use the empty tree and singleton tree respectively; these conventional degenerate cases have width zero. Every valid target decomposition is accepted.

Finite indices are zero based. Numerical data use Q001's self-delimiting binary
encoding unless the source explicitly requires unary. `none` means no valid
witness exists; it never means a program error. Construction and recovery must
be deterministic polynomial-time TM2 computations with polynomial output bounds,
as in Q001. Recovery is universal over valid target outputs and receives the
original source instance as well. Legal-instance predicates are specifications,
not algorithms the proposed reduction must execute.

## Build and verification

Lean 4.35.0 and matching Mathlib are pinned by `lean-toolchain`, `lakefile.toml`
and `lake-manifest.json`. In this directory run:

```sh
lake exe cache get Mathlib.Computability.TuringMachine.Computable
LEAN_NUM_THREADS=2 lake build
lake env lean Audit.lean
./scripts/verify-comparator.sh
```

The comparator script and repository-root Linux CI follow the pinned Q001
reference. They run the bundled `lake comparator` with the strict axiom policy,
then, for an unfilled solution, require full statement agreement and rejection
only for `sorryAx`. Green CI verifies an open template, not a completed proof.
The script needs Linux and bubblewrap; macOS compilation is not comparator
verification. `Tests.lean` checks finite boundary examples, not general semantic
equivalence. Human review of the problem statement remains necessary.

## Provenance and license

Infrastructure follows Q001 at `6e5d9d7aa425db5f01ee44f4c4e1710cf2993fda`.
The files in this formal project are licensed under Apache-2.0; see `LICENSE`.
This does not change licensing of other files in the research repository.

Local verification results are recorded in `evidence/statement/verification.json`.
The comparator prerequisite test passes on macOS; its real Linux verdict cases
are skipped, and the comparator script itself exits at the missing `bwrap` prerequisite.
