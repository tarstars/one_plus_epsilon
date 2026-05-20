# one_plus_epsilon

This project checks a small constructive fact about a 17th root of unity.

Let `eps` be a primitive 17th root of unity. In other words:

```text
eps^17 = 1
eps != 1
Phi_17(eps) = 1 + eps + eps^2 + ... + eps^16 = 0
```

Then `(1 + eps)^(-1)` is again an integer-coefficient polynomial in
`eps`:

```text
(1 + eps)^(-1) = -eps - eps^3 - eps^5 - ... - eps^15
```

The proof is just multiplication:

```text
(1 + x)(-x - x^3 - ... - x^15)
  = -(x + x^2 + ... + x^16)
  = 1 - Phi_17(x)
```

The last line has no constant term because
`1 - Phi_17(x) = 1 - (1 + x + ... + x^16)`.

After substituting `x = eps`, the `Phi_17(eps)` term vanishes, so the
product is `1`.

## Why the primitive assumption matters

If we only impose `x^17 = 1`, then `x = 1` is still allowed. In the quotient
`Z[x] / (x^17 - 1)`, `(1 + x)` has no integer-coefficient inverse: evaluating
at `x = 1` would require `2q(1) = 1`.

Over rational coefficients the larger quotient does have:

```text
(1 + x)(1 - x + x^2 - ... + x^16) = 1 + x^17 = 2
```

so the inverse is half of the alternating polynomial. The program prints this
contrast explicitly.

## Run

The project has no third-party dependencies.

```bash
python -m one_plus_epsilon
```

Useful options:

```bash
python -m one_plus_epsilon --trace-conjugates
python -m one_plus_epsilon --powers 20
python -m one_plus_epsilon --degree 17
```

`--trace-conjugates` multiplies the factors
`(1 + eps), (1 + eps^2), ..., (1 + eps^16)` one by one and reduces after each
step. The final product is `1`, giving another constructive view:

```text
product_{k=1}^{16} (1 + eps^k) = 1
```

Therefore:

```text
(1 + eps)^(-1) = product_{k=2}^{16} (1 + eps^k)
```

`--powers N` instead repeatedly multiplies by the same factor `(1 + eps)`.
This is useful for checking the tempting but different experiment of looking
for a power of `(1 + eps)` that becomes a constant.

## Test

```bash
python -m unittest discover -s tests
```

## Project layout

```text
one_plus_epsilon/
  cli.py              command-line checker
  polynomial.py       exact polynomial arithmetic
  root_of_unity.py    17th-root constructions
docs/
  constructive_proof.md
tests/
  test_root_of_unity.py
```
