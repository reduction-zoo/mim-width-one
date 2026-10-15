module

public import Mathlib.Computability.TuringMachine.Computable

@[expose] public section

namespace MimWidthOne

/-- Q001's self-delimiting binary natural; length is logarithmic, not unary. -/
def encodeNat (n : Nat) : List Bool :=
  let bits := (Nat.toDigits 2 n).map (fun c => c == '1')
  List.replicate bits.length true ++ [false] ++ bits

def encodeList {α : Type} (encode : α → List Bool) (xs : List α) : List Bool :=
  encodeNat xs.length ++ xs.flatMap encode

def encodeOption {α : Type} (encode : α → List Bool) : Option α → List Bool
  | none => [false]
  | some x => true :: encode x

/-- None denotes mathematical nonexistence, never an execution error. -/
def searchOutput {I W : Type} (legal : I → Bool) (witness : I → W → Bool)
    (x : I) : Option W → Prop
  | some w => legal x = true ∧ witness x w = true
  | none => legal x = true ∧ ¬ ∃ w, witness x w = true

/-- Relational version for witnesses with quantified real or optimality conditions. -/
def relationalOutput {I W : Type} (legal : I → Bool) (witness : I → W → Prop)
    (x : I) : Option W → Prop
  | some w => legal x = true ∧ witness x w
  | none => legal x = true ∧ ¬ ∃ w, witness x w

structure Graph where
  n : Nat
  edges : List (Nat × Nat)
  deriving Repr

def adjacent (g : Graph) (u v : Nat) : Bool :=
  g.edges.any (fun e => (e.1 == u && e.2 == v) || (e.1 == v && e.2 == u))

def simple (g : Graph) : Bool :=
  g.edges.all (fun e => e.1 < g.n && e.2 < g.n && e.1 != e.2) &&
  decide ((g.edges.map (fun e => (min e.1 e.2, max e.1 e.2))).Nodup)

/-- Vertices at distance at most the supplied bound, including the starting set. -/
def ballFrom (g : Graph) : Nat → List Nat → List Nat
  | 0, seen => seen
  | k + 1, seen => ballFrom g k ((List.range g.n).filter (fun v =>
      seen.contains v || seen.any (fun u => adjacent g u v)))

def connected (g : Graph) : Bool :=
  g.n > 0 && (ballFrom g g.n [0]).length == g.n

def diameterAtMost (g : Graph) (d : Nat) : Bool :=
  (List.range g.n).all (fun v => (ballFrom g d [v]).length == g.n)

def radiusAtMost (g : Graph) (r : Nat) : Bool :=
  (List.range g.n).any (fun v => (ballFrom g r [v]).length == g.n)

def boolWords : Nat → List (List Bool)
  | 0 => [[]]
  | n + 1 => (boolWords n).flatMap (fun xs => [false :: xs, true :: xs])

def bipartite (g : Graph) : Bool :=
  (boolWords g.n).any (fun side => g.edges.all (fun e => side[e.1]? != side[e.2]?))

def crossingDegree (g : Graph) (side : List Bool) (v : Nat) : Nat :=
  ((List.range g.n).filter (fun u => adjacent g u v && side[u]? != side[v]?)).length

def nontrivialCut (g : Graph) (side : List Bool) : Bool :=
  side.length == g.n && side.contains true && side.contains false

def perfectCut (g : Graph) (side : List Bool) : Bool :=
  nontrivialCut g side && (List.range g.n).all (fun v => crossingDegree g side v == 1)

def boundedCut (g : Graph) (d : Nat) (side : List Bool) : Bool :=
  nontrivialCut g side && (List.range g.n).all (fun v => crossingDegree g side v ≤ d)

def encodeGraph (g : Graph) : List Bool :=
  encodeList encodeNat (List.range g.n) ++
  encodeList (fun e => encodeNat e.1 ++ encodeNat e.2) g.edges

def tree (g : Graph) : Bool := simple g &&
  (if g.n == 0 then g.edges.isEmpty else connected g && g.edges.length == g.n-1)
def degree (g : Graph) (v : Nat) := ((List.range g.n).filter (adjacent g v)).length
structure LeafTree where
  graph : Graph
  labels : List Nat
  deriving Repr
def leafTree (n : Nat) (t : LeafTree) : Bool := tree t.graph &&
  t.labels.length == n && decide t.labels.Nodup && t.labels.all (· < t.graph.n) &&
  (List.range t.graph.n).all (fun v => t.labels.contains v == (degree t.graph v ≤ 1))
def side (g : Graph) (i : Nat) : List Nat :=
  ballFrom ⟨g.n,(g.edges.zipIdx.filter (fun (_,j) => i != j)).map Prod.fst⟩ g.n [(g.edges[i]?.getD (0,0)).1]
structure Quartet where
  a : Nat
  b : Nat
  c : Nat
  d : Nat
  deriving Repr
structure Source where
  taxa : Nat
  quartets : List Quartet
  deriving Repr
def legalSource (x : Source) : Bool := x.quartets.all (fun q =>
  [q.a,q.b,q.c,q.d].all (· < x.taxa) && decide [q.a,q.b,q.c,q.d].Nodup)
def displays (t : LeafTree) (q : Quartet) : Bool := (List.range t.graph.edges.length).any (fun i =>
  let s := side t.graph i
  let member := fun v => s.contains (t.labels[v]?.getD t.graph.n)
  member q.a == member q.b && member q.c == member q.d && member q.a != member q.c)
def sourceWitness (x : Source) (t : LeafTree) : Bool := leafTree x.taxa t && x.quartets.all (displays t)
def legalTarget := simple
/-- Only cross edges of the cut graph count as edges of an induced matching. -/
def cutWidthOne (g : Graph) (s : List Nat) : Bool :=
  (List.range g.n).all (fun a => (List.range g.n).all (fun b =>
    (List.range g.n).all (fun c => (List.range g.n).all (fun d =>
      !(decide [a,b,c,d].Nodup && s.contains a && !s.contains b && s.contains c && !s.contains d &&
        adjacent g a b && adjacent g c d) || adjacent g a d || adjacent g c b))))
def targetWitness (g : Graph) (t : LeafTree) : Bool := leafTree g.n t &&
  (List.range t.graph.n).all (fun v => degree t.graph v ≤ 3) &&
  (List.range t.graph.edges.length).all (fun i =>
    cutWidthOne g ((List.range g.n).filter (fun v => (side t.graph i).contains (t.labels[v]?.getD t.graph.n))))
def validSourceOutput := searchOutput legalSource sourceWitness
def validTargetOutput := searchOutput legalTarget targetWitness
def encodeSource (x : Source) := encodeList encodeNat (List.range x.taxa) ++
  encodeList (fun q => encodeNat q.a ++ encodeNat q.b ++ encodeNat q.c ++ encodeNat q.d) x.quartets
def encodeTarget := encodeGraph
def encodeWitness (t : LeafTree) := encodeGraph t.graph ++ encodeList encodeNat t.labels

/-- Both algorithms use Q001's explicit bit encoding and TM2 cost model.
Recovery receives the full pair of source instance and target output. -/
def Reduction (forward : Source → Graph)
    (recover : Source × Option LeafTree → Option LeafTree) : Prop :=
  Nonempty (Turing.TM2ComputableInPolyTime encodeSource encodeTarget forward) ∧
  Nonempty (Turing.TM2ComputableInPolyTime
    (fun input => encodeSource input.1 ++ (encodeOption encodeWitness) input.2)
    (encodeOption encodeWitness) recover) ∧
  (∃ bound : Polynomial Nat, ∀ x,
    (encodeTarget (forward x)).length ≤ bound.eval (encodeSource x).length) ∧
  (∃ bound : Polynomial Nat, ∀ input,
    ((encodeOption encodeWitness) (recover input)).length ≤
      bound.eval (encodeSource input.1 ++ (encodeOption encodeWitness) input.2).length) ∧
  (∀ x, legalSource x = true → legalTarget (forward x) = true) ∧
  (∀ x, legalSource x = true → ∀ y, validTargetOutput (forward x) y →
    validSourceOutput x (recover (x, y)))


def Goal : Prop :=
  ∃ (forward : Source → Graph)
    (recover : Source × Option LeafTree → Option LeafTree), Reduction forward recover

/-- Open question only; this placeholder is not a solution. -/
theorem solve : Goal := by
  sorry

end MimWidthOne
