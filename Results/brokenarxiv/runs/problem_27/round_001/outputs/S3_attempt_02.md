1. Assignment restatement

Prove SC4: once S2 has produced a sequence of Bruhat intervals with some growing finite-poset invariant, show that this invariant is preserved under finite-poset isomorphism. Also identify the invariant used by S2.

2. Subproof or failure

This subproblem depends explicitly on S2’s construction. The prompt does not supply S2’s invariant, so I cannot honestly identify “exactly which invariant from S2 is used.”

Conditional preservation lemma:

Let \(P,Q\) be finite posets and let \(\varphi:P\to Q\) be a poset isomorphism. Any quantity defined purely from the order relation of the finite poset is preserved by \(\varphi\).

For example, if S2’s invariant is one of the following, then it is preserved:

- total number of elements;
- number of elements of a given rank in a graded interval;
- number of maximal chains;
- number of atoms or coatoms;
- size of an antichain defined order-theoretically;
- the rank-generating function;
- any incidence count among comparable pairs or covering relations.

Proof: A poset isomorphism is a bijection \(\varphi:P\to Q\) such that
\[
x\le_P y \iff \varphi(x)\le_Q \varphi(y).
\]
Hence it preserves and reflects all order-theoretic relations: comparability, incomparability, minimality, maximality, covering relations, chain membership, antichain membership, and ranks in graded intervals. Therefore any invariant expressible solely in terms of these relations has the same value on \(P\) and \(Q\). Thus if S2 constructs intervals whose chosen order-theoretic invariant takes infinitely many values, those intervals cannot fall into finitely many finite-poset isomorphism types.

This proves SC4 conditionally, but not with the requested exact identification, because S2’s invariant is absent from the packet.

3. Solver failure output and candidate guidance

```yaml
solved: false
unsolved: "Cannot identify the exact invariant from S2 because S2's construction and invariant are not supplied in the prompt."
conditional_result: "Any finite-poset invariant defined purely from the order relation is preserved under finite-poset isomorphism."
candidate_guidance: "S2 should explicitly name an order-theoretic invariant, such as a rank-size number, number of atoms/coatoms, number of maximal chains, or another finite-poset statistic, and show it is unbounded along its constructed fixed-length intervals."
```

4. Local Source Ledger

Used only standard background: definition of finite poset isomorphism and the elementary fact that an isomorphism preserves first-order order-theoretic structure. No Coxeter-specific theorem was used.

5. Interface notes for S6

S6 may use the conditional SC4 lemma once S2 supplies a concrete invariant. The invariant must be visibly defined from the interval as a finite poset, not from labels \(u,v\), reduced words, or ambient Coxeter-group data unless S2 proves that data is recoverable from the poset structure.

6. Web-source confirmation

No web search, internet, files, tools, APIs, or prior history were used.