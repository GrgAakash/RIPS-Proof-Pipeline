## 1. Assignment Restatement

For a fixed ordered oriented-transversal component with order  
`A_1 ≺ ... ≺ A_m`, prove the global affine chart lemma:

Choose a linear functional `lambda` using the separation of `A_1` and `A_m`, equivalently using the difference body `A_m - A_1`, such that every oriented transversal in this order has positive `lambda`-direction. Then every such oriented line can be uniquely normalized as

```text
ell(t) = p + t v,
lambda(p) = 0,
lambda(v) = 1.
```

## 2. Subproof Or Failure

Let `A_1,...,A_m` be pairwise disjoint open convex sets, and fix an oriented line transversal whose induced order is

```text
A_1 ≺ A_2 ≺ ... ≺ A_m.
```

Since `A_1` and `A_m` are disjoint open convex sets, the open convex set

```text
A_m - A_1 = {a_m - a_1 : a_m in A_m, a_1 in A_1}
```

does not contain `0`. Indeed, `0 in A_m - A_1` would mean some `a_m = a_1`, contradicting disjointness.

By the standard separation theorem for the open convex set `A_m - A_1` and the point `0`, there exists a nonzero linear functional `lambda` such that

```text
lambda(w) > 0      for every w in A_m - A_1.
```

Equivalently,

```text
lambda(a_m) > lambda(a_1)
```

for every `a_1 in A_1` and `a_m in A_m`.

Now take any oriented transversal `ell` in the fixed order component. Write it with any affine oriented parametrization

```text
ell(s) = q + s u,
```

where positive `s` is the chosen orientation. Since the line meets `A_1` before `A_m`, there are parameters `s_1 < s_m` with

```text
q + s_1 u in A_1,
q + s_m u in A_m.
```

Set

```text
a_1 = q + s_1 u,
a_m = q + s_m u.
```

Then

```text
a_m - a_1 = (s_m - s_1)u in A_m - A_1.
```

Applying the choice of `lambda` gives

```text
0 < lambda(a_m - a_1)
  = (s_m - s_1) lambda(u).
```

Since `s_m - s_1 > 0`, it follows that

```text
lambda(u) > 0.
```

Thus every oriented transversal in this fixed order has positive `lambda`-direction.

Therefore each such oriented line has a unique normalized representative. Given any oriented affine parametrization `ell(s)=q+s u` with `lambda(u)>0`, define

```text
v = u / lambda(u),
p = q - lambda(q) v.
```

Then

```text
lambda(v) = 1
```

and

```text
lambda(p) = lambda(q) - lambda(q)lambda(v) = 0.
```

So the same oriented line is written as

```text
ell(t) = p + t v,
lambda(p)=0,
lambda(v)=1.
```

Uniqueness: if

```text
p + t v
```

and

```text
p' + t v'
```

are two normalized parametrizations of the same oriented line with `lambda(p)=lambda(p')=0` and `lambda(v)=lambda(v')=1`, then their direction vectors represent the same positive oriented direction. Hence `v' = c v` for some `c>0`; applying `lambda` gives `1 = c`, so `v'=v`. Then `p'` lies on the same line, so `p'=p+s v` for some `s`; applying `lambda` gives `0 = 0+s`, hence `s=0`, so `p'=p`.

This proves the separating-functional/global-chart lemma.

## 3. YAML Failure Output/Candidate Guidance

```yaml
status: success
failure: null
candidate_guidance:
  separating_functional:
    source: "Separate the open convex set A_m - A_1 from 0."
    conclusion: "lambda(a_m - a_1) > 0 for all a_i in A_i."
  chart:
    condition: "Every oriented transversal in the fixed order has lambda(direction) > 0."
    normalization: "p = q - lambda(q)u/lambda(u), v = u/lambda(u)."
```

## 4. Local Source Ledger

```yaml
sources_used:
  - prompt
  - standard finite-dimensional convex separation theorem
external_sources: []
code_or_computation: none
```

## 5. Interface Notes For S6

The chart identifies the fixed-order oriented transversal space with a subset of the affine space

```text
H x {v : lambda(v)=1},
where H = {p : lambda(p)=0}.
```

Under this chart, intersection with `A_i` can be expressed by the existence of a time parameter `t_i` such that

```text
p + t_i v in A_i.
```

For the fixed order, the relevant times satisfy

```text
t_1 < ... < t_m.
```

The key point exported to later stages is that no line in this ordered component has `lambda(v)=0` or negative `lambda(v)`, so the chart is global on the whole fixed-order oriented component.

## 6. Web-Source Confirmation

No web sources were used, per the assignment constraint.