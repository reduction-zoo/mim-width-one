# Unrooted Quartet Consistency → Mim-width at most one

Category: Complexity open

## Source

The source is a finite collection of labelled quartet trees. Its outputs are unrooted trees displaying every prescribed quartet, or NO-SOLUTION.

## Target

The source asks for a tree displaying a collection of prescribed unrooted quartets. The target asks for a branch decomposition of a graph such that every cut has bipartite induced matching number at most one.

## Required result

Construct deterministic polynomial-time maps F and G: F sends every legal source instance to a legal target instance, and G(x,y) is a valid source output for every valid output y of F(x). Preserve the stated threshold, domain and promises. The requested complexity conclusion is NP-hardness for the stated target problem.

## Acceptance

Give explicit construction and recovery algorithms, a general proof for every legal input and every valid target output, and polynomial runtime and encoding-size bounds. Specify finite output encodings and handle NO-SOLUTION outputs when applicable. Tests compare recovered source outputs with independent source solutions.

## Why it matters

Width-one recognition concerns the simplest nontrivial level of a width measure used for graph algorithms.

## Difficulty

A construction must force a compatible decomposition tree rather than only exhibit one for positive instances.

## Literature context

The cited width-recognition question concerns induced matchings across decomposition cuts. Results about related width measures cannot be substituted for mim-width one.

Literature checked 2026-09-16. This summarizes the archived literature search on the date above. Unpublished, unindexed and overlooked work remains outside coverage; no new novelty assessment was performed.

## References

- [On the Hardness of Recognizing Graphs of Small Mim-Width and Its Variants](https://drops.dagstuhl.de/storage/00lipics/lipics-vol374-icalp2026/html/LIPIcs.ICALP.2026.83/LIPIcs.ICALP.2026.83.html): Dupré la Tour, Lafond and Ndiaye, On the Hardness of Recognizing Graphs of Small Mim-Width and Its Variants, Theorems 1–2, proves hardness for sim-width one and mim-width at most two. Section 5 explicitly leaves mim-width one and its linear version open. Section 3 constructs a graph from quartets using two three-edge paths per quartet and complete joins between auxiliary vertices of different quartets. Proposition 6 supplies the sim-width and one-sided-width implications, not a mim-width-one implication.
- [arXiv record](https://arxiv.org/abs/2512.06186): On 2026-09-16 checked the conference paper and arXiv record, and searched "mim-width 1" recognition 2026 and "mim-width" "one" "recognition" polynomial 2026. No later resolution was identified within this coverage. The distinction between induced matchings in the whole graph and in the cut graph is decisive: within-side edges disappear in the latter. Existing hardness for the larger class does not establish recognition hardness for its width-one subclass.

Fixed from board record `website/questions/mim-width-one.json` in board checkout at 6c7d3bd9c0a8f595279969a9c0a4d1853a3f5c17; the record was copied from the current working tree.
