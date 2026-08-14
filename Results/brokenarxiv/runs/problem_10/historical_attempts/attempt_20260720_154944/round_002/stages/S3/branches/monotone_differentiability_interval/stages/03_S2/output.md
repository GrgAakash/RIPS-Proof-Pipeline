**1. Assignment Restatement**

Branch S2 proves only the unary weak-o-minimal consequences needed downstream.

Given a definable set `A subset J`, prove:

1. If `A` meets every nonempty open subinterval of some nonempty open `U subset J`, then `A` contains a nonempty open interval, in fact one contained in `U`.
2. If `A` has empty interior in `J`, then `A` is finite, hence locally finite/discrete in the needed interval sense.

**2. Subproof Or Failure**

Solved.

Call a set `C subset M` convex if whenever `a<c<b` and `a,b in C`, then `c in C`.

**Lemma S2.1: Convex sets with two points contain intervals.**  
If `C subset M` is convex and contains `a<b`, then `(a,b) subset C`. Since `M` is an ordered field, `(a,b)` is nonempty, for example it contains `(a+b)/2`. Thus a convex set with empty interior has at most one point.

**Lemma S2.2: Unary definable dichotomy.**  
Let `A subset J` be definable. By weak o-minimality,

`A = C_1 union ... union C_n`

with each `C_i` convex. If some `C_i` contains two points `a<b`, then `(a,b) subset C_i subset A`, so `A` contains a nonempty open interval. Otherwise every `C_i` has at most one point, so `A` is finite.

Therefore:

`A` has empty interior in `J` iff `A` is finite.

More precisely, if `A` contains no nonempty open interval contained in `J`, then `A` is finite.

**Lemma S2.3: Interval-density forces interior.**  
Let `U subset J` be nonempty open, and suppose `A subset J` is definable and meets every nonempty open interval `I subset U`.

Choose a nonempty open interval `I_0 subset U`. The set `A cap I_0` is definable. By Lemma S2.2, either it is finite or it contains a nonempty open interval.

It cannot be finite: a finite subset of an ordered field cannot meet every nonempty open subinterval of `I_0`, since any nonempty open interval contains further open intervals avoiding a given finite set. Hence `A cap I_0` contains a nonempty open interval `V`.

Thus:

`V subset A cap U`.

So `A` contains a nonempty open interval inside `U`.

**Lemma S2.4: Empty-interior definable sets are locally finite.**  
Let `A subset J` be definable with empty interior. By Lemma S2.2, `A` is finite.

Hence for every `p in J`, there is an open interval `W subset J` with `p in W` such that

`W cap A subset {p}`.

Indeed, remove `p` from the finite set `A`. Choose the nearest remaining point below `p`, if one exists, and the nearest remaining point above `p`, if one exists; otherwise choose any endpoints inside `J` on the relevant side of `p`. The resulting interval around `p` avoids `A \ {p}`.

Consequences used downstream:

- If `p notin A`, then some open neighborhood of `p` is disjoint from `A`.
- Every nonempty open interval `I subset J` contains a nonempty open subinterval `I' subset I` with `I' cap A = empty`.
- A definable empty-interior bad set cannot be interval-dense anywhere.

**3. YAML**

```yaml
failure_output_type: solved
output_type: branch_lemma
branch: S2
status: solved
main_exports:
  - S2.2 unary definable dichotomy: finite or contains interval
  - S2.3 interval-density implies contains open interval
  - S2.4 empty-interior definable sets are finite and locally avoidable
```

**4. Local Source Ledger**

Used only:

- Supplied weak o-minimality: every unary definable subset of `M` is a finite union of convex sets.
- Ordered-field order algebra: if `a<b`, then `(a+b)/2` lies in `(a,b)`.
- Ordered-field topology: nonempty open intervals contain smaller nonempty open intervals.
- Basic closure of definability under intersection with parameter-definable intervals.

No external theorems used.

**5. Interface Notes For Branch S6**

S6 may use the following as black-box branch outputs:

- If a definable bad set `B subset J` is shown to meet every open subinterval of some open `U`, then S2 upgrades this to an actual nonempty open interval `V subset U` with `V subset B`.
- If another branch proves that `B` contains no nonempty open interval, then S2 immediately gives `B` finite.
- Once `B` is finite, S2 gives a nonempty open interval avoiding `B`, which is the needed local-clean interval for assembly.

**6. Web-Source Confirmation**

No web or external sources were used, in accordance with the branch packet.