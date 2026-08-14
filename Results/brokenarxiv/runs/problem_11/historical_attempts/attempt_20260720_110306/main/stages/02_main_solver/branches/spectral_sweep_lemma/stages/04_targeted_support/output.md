**1. Verdict**

BLOCK. The displayed inequality is false as stated. There is no absolute constant `K`.

**2. Counterexample Family**

For any integer `m >= 2`, set `N = m`, choose

```text
y = (1, m^{-1/2}, ..., m^{-1/2})  with m-1 small entries,
D = 1 / (2 sqrt(m)).
```

Then, up to measure-zero endpoints,

```text
n(t) = m  for 0 < t <= a,
n(t) = 1  for a < t <= 1,
n(t) = 0  for t > 1,
```

where `a = m^{-1/2}`.

**3. LHS Computation**

For `0 < t <= a`, the integrand is `min{m^2, m} = m`.

For `a < t <= 1`:
- if `0 < s <= a`, the integrand is `min{m, m} = m`;
- if `a < s < t`, the integrand is `min{1, m^{-1/2}} = m^{-1/2}`.

Thus

```text
LHS
= m a^2 + 2m a(1-a) + m^{-1/2}(1-a)^2.
```

With `a = m^{-1/2}`,

```text
LHS = 2 sqrt(m) - 1 + m^{-1/2} - 2m^{-1} + m^{-3/2}.
```

**4. RHS Normalizer**

```text
∫_0^∞ 2t n(t) dt
= m a^2 + (1 - a^2)
= 2 - 1/m.
```

Also `D sqrt(N) = 1/2`, so the RHS without `K` is

```text
D sqrt(N) ∫_0^∞ 2t n(t) dt
= 1 - 1/(2m).
```

Therefore the required `K` would have to satisfy

```text
K >= [2 sqrt(m) - 1 + m^{-1/2} - 2m^{-1} + m^{-3/2}]
     / [1 - 1/(2m)].
```

This tends to infinity as `m -> ∞`.

**5. Failure Mechanism**

The obstruction is a short high-multiplicity layer followed by a long singleton tail. The cross-region `s <= a < t` contributes about `2 sqrt(N)` to the LHS, while the RHS normalizer stays about constant when `D sqrt(N) = 1/2`.

**6. Salvage**

A nearby true bound is obtained if the second term uses the lower layer size:

```text
2 ∫∫_{s<t} min{n(s)n(t), 2D n(t)^{3/2}} ds dt
<= 2D sqrt(N) ∫_0^∞ 2t n(t) dt.
```

Indeed, since `n(t) <= N`,

```text
min{n(s)n(t), 2D n(t)^{3/2}} <= 2D sqrt(N) n(t),
```

and integrating `s` over `[0,t]` gives the constant `K = 2` for that modified inequality.