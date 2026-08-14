## 1. Assignment Restatement

Finish only the unoriented reduction step for Problem 39.

Assume the S0/S5 inputs already established:

- For every fixed order `sigma`, each connected component of the oriented fixed-order transversal space `T_sigma` is acyclic.
- The oriented transversal space decomposes by fixed orders.
- The forget-orientation map from oriented lines to unoriented lines is a double cover.
- For any connected component `K` of the unoriented transversal space, its lift is either one acyclic component mapping homeomorphically to `K`, or two acyclic components forming a trivial two-sheeted cover over `K`.

## 2. Subproof Or Failure

Let `L` be the space of unoriented line transversals to the given family, and let `L^+` be the corresponding space of oriented line transversals. Let

```text
q : L^+ -> L
```

be the map forgetting orientation.

Fix a connected component `K` of `L`. Since `q` is a covering map, `q^{-1}(K)` is a union of connected components of `L^+`. By the fixed-order decomposition, every connected component of `L^+` lies inside some fixed-order piece `T_sigma`; by the oriented result, each such component is acyclic.

Now there are two cases.

First, if `q^{-1}(K)` is connected, then by the assigned hypothesis it maps homeomorphically onto `K`. Therefore `K` is homeomorphic to an acyclic space, hence is acyclic.

Second, if `q^{-1}(K)` has two connected components, say

```text
q^{-1}(K) = A ⊔ B,
```

then the assigned double-cover hypothesis says this is a trivial two-sheeted cover over `K`. In particular, each sheet maps homeomorphically onto `K`:

```text
q|_A : A -> K,
q|_B : B -> K.
```

Since `A` and `B` are connected components of the oriented transversal space, each is acyclic. Hence `K`, being homeomorphic to `A` for example, is acyclic.

Thus every connected component of the unoriented transversal space is acyclic.

## 3. YAML Failure Output/Candidate Guidance

```yaml
status: success
failure: null
candidate_guidance:
  - The unoriented step is complete assuming the stated oriented fixed-order acyclicity and the stated lift dichotomy.
  - No additional local convexity or incidence-space filling argument is used here.
  - The only remaining dependencies belong upstream: proving acyclicity of fixed-order oriented components and verifying the cover/lift dichotomy.
```

## 4. Local Source Ledger

```yaml
used_sources:
  - user_prompt
  - standard_background:
      - covering-space facts
      - homeomorphism invariance of homology
      - fixed-order decomposition of oriented line transversals
```

## 5. Interface Notes For S6

S6 may take as established:

```yaml
unoriented_reduction:
  input_needed:
    - each connected component of each oriented fixed-order piece T_sigma is acyclic
    - forget-orientation map L_plus -> L is a double cover
    - for each connected unoriented component K, q^{-1}(K) is either:
        - one acyclic component mapping homeomorphically to K
        - two acyclic components forming a trivial two-sheeted cover of K
  output:
    - every connected component K of the unoriented transversal space is acyclic
```

## 6. Web-Source Confirmation

No web, internet, API keys, memory, prior files, code execution, CAS, or simulations were used.