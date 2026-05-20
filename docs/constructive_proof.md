# Constructive proof

Let `eps` be a primitive 17th root of unity. The primitive assumption means:

```text
Phi_17(eps) = 1 + eps + eps^2 + ... + eps^16 = 0
```

We want an integer-coefficient polynomial `q(x)` such that:

```text
(1 + eps) q(eps) = 1
```

Take:

```text
q(x) = -x - x^3 - x^5 - x^7 - x^9 - x^11 - x^13 - x^15
```

Then:

```text
(1 + x) q(x)
  = -x - x^2 - x^3 - ... - x^16
  = 1 - (1 + x + x^2 + ... + x^16)
  = 1 - Phi_17(x)
```

This is the point where the expression can look suspicious: the constant
term is zero on both sides, since the `1 - 1` cancels.

Substitute `x = eps`:

```text
(1 + eps) q(eps) = 1 - Phi_17(eps) = 1
```

So:

```text
(1 + eps)^(-1)
  = -eps - eps^3 - eps^5 - eps^7
    - eps^9 - eps^11 - eps^13 - eps^15
```

## Conjugate-product version

The same inverse can also be found by multiplying conjugate factors. Since:

```text
Phi_17(x) = product_{k=1}^{16} (x - eps^k)
```

we get:

```text
Phi_17(-1)
  = product_{k=1}^{16} (-1 - eps^k)
```

There are 16 factors, so the sign disappears:

```text
product_{k=1}^{16} (1 + eps^k) = Phi_17(-1)
```

For an odd prime `p`, `Phi_p(x) = 1 + x + ... + x^(p-1)`, hence:

```text
Phi_17(-1) = 1 - 1 + 1 - ... + 1 = 1
```

Therefore:

```text
product_{k=1}^{16} (1 + eps^k) = 1
```

and:

```text
(1 + eps)^(-1) = product_{k=2}^{16} (1 + eps^k)
```

The command:

```bash
python -m one_plus_epsilon --trace-conjugates
```

prints this multiplication step by step, reducing every intermediate product
modulo `Phi_17(x)`.

## Why `x^17 = 1` alone is not enough

If the only relation is `x^17 = 1`, then `x = 1` is included. An integer
inverse would be a polynomial `q(x)` satisfying:

```text
(1 + x)q(x) = 1 mod (x^17 - 1)
```

Evaluating at `x = 1` gives:

```text
2q(1) = 1
```

This is impossible for integer coefficients, since `q(1)` is an integer.

Over rational coefficients the obstruction disappears:

```text
(1 + x)(1 - x + x^2 - ... + x^16) = 1 + x^17
```

Modulo `x^17 = 1`, this product is `2`, so:

```text
(1 + x)^(-1)
  = (1/2)(1 - x + x^2 - ... + x^16)
```

in `Q[x] / (x^17 - 1)`.
