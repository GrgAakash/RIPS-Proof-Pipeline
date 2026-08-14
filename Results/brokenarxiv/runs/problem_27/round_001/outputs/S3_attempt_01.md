1. **Assignment**

SC4 cannot be proved from the packet as stated.

The assignment says: “Prove SC4. Identify exactly which invariant from S2 is used and prove it is preserved by finite-poset isomorphism.” But the prompt supplies neither:

- the statement of `SC4`, nor
- the invariant established in `S2`.

So the required dependency is unavailable.

2. **Conditional SC4 Form**

A valid SC4 proof would have the following shape:

Let `I([u,v])` be the invariant supplied by S2 for finite Bruhat intervals. If S2 proves that an infinite irreducible Coxeter group produces infinitely many length-`k` intervals with pairwise distinct values of `I`, then SC4 may conclude that these intervals have pairwise non-isomorphic finite posets, provided `I` is preserved under finite-poset isomorphism.

3. **Isomorphism Preservation**

The invariant used from S2 must be expressible purely in the language of finite posets. Examples of sufficient invariants include:

- number of elements in the interval,
- rank numbers,
- number of maximal chains,
- number of elements covering the bottom element,
- number of elements covered by the top element,
- full cover graph up to graph isomorphism,
- Möbius function of the interval,
- any statistic definable only from the order relation.

If `φ : P -> Q` is a finite-poset isomorphism, then for all `x,y in P`,

```text
x <=_P y  iff  φ(x) <=_Q φ(y).
```

Therefore every invariant computed solely from the order relation is preserved by `φ`. Hence if two intervals have different values of such an invariant, they cannot be isomorphic as finite posets.

4. **Dependency**

The proof of SC4 depends on S2 providing an invariant `I` satisfying both:

```text
I([u_n,v_n]) are infinitely many distinct values;
I is determined entirely by the finite poset structure of [u_n,v_n].
```

Without that, SC4 is not independently provable from the current packet.

5. **YAML Failure Output**

```yaml
status: failed
reason: missing_dependency
missing_items:
  - statement_of_SC4
  - invariant_from_S2
conditional_result: >
  If S2 supplies a finite-poset invariant taking infinitely many values on
  length-k Bruhat intervals, then SC4 follows because finite-poset isomorphisms
  preserve all order-theoretic invariants.
fabricated_proof: false
```

6. **Ledger / Interface Notes / Web Confirmation**

Local source ledger: only the mathematical content in the user prompt was used.

Interface notes: SC4 should explicitly cite the S2 invariant by name and show it is order-theoretic.

Web-source confirmation: no web search or internet sources were used, per instruction.