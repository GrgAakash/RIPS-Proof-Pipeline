CLEANED SKELETON PACKET FOR THIS RUN

Definitions/notation allowed for parsing the target:
- An algebraic torus T over Q is a Q-group that becomes isomorphic to a power of G_m over a finite extension of Q.
- For a prime p, Q_p is the p-adic field.
- T(Q_p) denotes the group of Q_p-points.
- T(Q) denotes the group of Q-points.
- T(Z_p) denotes the maximal compact subgroup of T(Q_p).

Formal statements before the target theorem: None.
Later-but-upstream inclusions: None.
Exclusions: None.
Unclear: None.

Target theorem:
For any algebraic torus T over Q and any prime number p, the decomposition T(Q_p) = T(Z_p)T(Q) holds, where T(Z_p) denotes the maximal compact subgroup of T(Q_p).
You are S5, a Subproblem Solver. Follow the fixed S1-S5 Subproblem Solver prompt exactly in structure: sections 1 through 6, including the YAML failure block and Local Source Ledger. Use no web, no external sources, no prior history.

Allowed supporting statements:
Definitions, notation, and assumptions needed to state or parse the target theorem are allowed.
No formal skeleton statement may be cited without reproof because there are no formal statements before the target theorem in this standalone packet.
Genuinely standard background may be used as permitted by the fixed solver prompt.

Target theorem:
For any algebraic torus T over Q and any prime number p, the decomposition T(Q_p) = T(Z_p)T(Q) holds, where T(Z_p) denotes the maximal compact subgroup of T(Q_p).

Additional mathematical guidance:
None

S0 blueprint:
C1: Choose a finite Galois splitting field K/Q for T, a place w | p, set G = Gal(K/Q), D = Gal(K_w/Q_p), and X = X^*(T_K). Then T(Q) = Hom_G(X, K^*) and T(Q_p) = Hom_D(X, K_w^*).
C2: For the local torus T/Q_p, the character-valuation map on T(Q_p) has kernel exactly T(Z_p), the maximal compact subgroup.
C3: For any t in T(Q_p), the local valuation homomorphism χ ↦ v_w(χ(t)) is realized by some rational point q in T(Q); that is, v_w(χ(q)) = v_w(χ(t)) for every χ in X.
C4: If t in T(Q_p) and q in T(Q) have identical local character valuations over K_w, then tq^{-1} belongs to T(Z_p).
C5: Every t in T(Q_p) can be written t = kq with k in T(Z_p) and q in T(Q).
Assignments:
S1: Prove C1 and C2.
S2: Prove C3.
S3: Prove C4.
S4: Assemble C3 and C4.
S5: Perform the final consistency audit: independence of the choice of K and w, compatibility with ramified and split cases, and confirmation that T(Z_p) is used only as maximal compact.

Assigned subproblem:
S5: Perform the final consistency audit: independence of the choice of K and w, compatibility with ramified and split cases, and confirmation that T(Z_p) is used only as maximal compact.