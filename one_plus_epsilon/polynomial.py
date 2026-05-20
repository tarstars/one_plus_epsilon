"""Small exact polynomial toolkit.

Polynomials are stored as tuples of ``Fraction`` coefficients in ascending
degree order:

    (a0, a1, a2) means a0 + a1*x + a2*x^2.

The code is intentionally lightweight. It is enough to make the root-of-unity
calculation auditable without pulling in a symbolic algebra dependency.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Iterable

Coeff = Fraction
Polynomial = tuple[Coeff, ...]


def poly(coefficients: Iterable[int | Fraction]) -> Polynomial:
    """Create a normalized polynomial from integer or rational coefficients."""

    return trim(tuple(Fraction(c) for c in coefficients))


def trim(coefficients: Iterable[Coeff]) -> Polynomial:
    """Remove trailing zero coefficients, preserving zero as ``(0,)``."""

    items = list(coefficients)
    while len(items) > 1 and items[-1] == 0:
        items.pop()
    if not items:
        return (Fraction(0),)
    return tuple(items)


def degree(p: Polynomial) -> int:
    """Return the degree of a nonzero polynomial, or -1 for zero."""

    p = trim(p)
    return -1 if p == (0,) else len(p) - 1


def add(left: Polynomial, right: Polynomial) -> Polynomial:
    """Add two polynomials."""

    size = max(len(left), len(right))
    result = [Fraction(0)] * size
    for i in range(size):
        if i < len(left):
            result[i] += left[i]
        if i < len(right):
            result[i] += right[i]
    return trim(result)


def sub(left: Polynomial, right: Polynomial) -> Polynomial:
    """Subtract ``right`` from ``left``."""

    size = max(len(left), len(right))
    result = [Fraction(0)] * size
    for i in range(size):
        if i < len(left):
            result[i] += left[i]
        if i < len(right):
            result[i] -= right[i]
    return trim(result)


def scale(p: Polynomial, factor: int | Fraction) -> Polynomial:
    """Multiply every coefficient by ``factor``."""

    factor = Fraction(factor)
    return trim(c * factor for c in p)


def mul(left: Polynomial, right: Polynomial) -> Polynomial:
    """Multiply two polynomials."""

    if left == (0,) or right == (0,):
        return (Fraction(0),)
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return trim(result)


def monomial(power: int, coefficient: int | Fraction = 1) -> Polynomial:
    """Return ``coefficient * x^power``."""

    if power < 0:
        raise ValueError("power must be non-negative")
    result = [Fraction(0)] * (power + 1)
    result[power] = Fraction(coefficient)
    return trim(result)


def one_plus_monomial(power: int) -> Polynomial:
    """Return ``1 + x^power``."""

    return add(poly([1]), monomial(power))


def reduce_mod_monic(p: Polynomial, modulus: Polynomial) -> Polynomial:
    """Reduce ``p`` modulo a monic polynomial.

    This is plain polynomial long division. The quotient is not returned
    because the root-of-unity checks only need the canonical remainder.
    """

    modulus = trim(modulus)
    if modulus == (0,):
        raise ValueError("modulus must be nonzero")
    if modulus[-1] != 1:
        raise ValueError("modulus must be monic")

    remainder = list(trim(p))
    modulus_degree = len(modulus) - 1

    while len(remainder) >= len(modulus) and remainder != [Fraction(0)]:
        lead = remainder[-1]
        shift = len(remainder) - len(modulus)
        if lead:
            for i, coefficient in enumerate(modulus):
                remainder[i + shift] -= lead * coefficient
        while len(remainder) > 1 and remainder[-1] == 0:
            remainder.pop()

    if len(remainder) > modulus_degree:
        raise RuntimeError("polynomial reduction failed")
    return trim(remainder)


def reduce_mod_xn_minus_one(p: Polynomial, n: int) -> Polynomial:
    """Reduce by the cyclic relation ``x^n = 1``."""

    if n <= 0:
        raise ValueError("n must be positive")
    result = [Fraction(0)] * n
    for power, coefficient in enumerate(p):
        result[power % n] += coefficient
    return trim(result)


def format_polynomial(p: Polynomial, variable: str = "x") -> str:
    """Format a polynomial for terminal output and docs."""

    p = trim(p)
    if p == (0,):
        return "0"

    parts: list[str] = []
    for power in range(len(p) - 1, -1, -1):
        coefficient = p[power]
        if coefficient == 0:
            continue
        sign = "-" if coefficient < 0 else "+"
        body = _format_term(abs(coefficient), power, variable)
        if not parts:
            parts.append(body if sign == "+" else f"-{body}")
        else:
            parts.append(f" {sign} {body}")
    return "".join(parts)


def coefficient_vector(p: Polynomial, width: int | None = None) -> str:
    """Return coefficients in ascending degree order."""

    p = trim(p)
    if width is not None:
        values = list(p) + [Fraction(0)] * max(0, width - len(p))
    else:
        values = list(p)
    return "[" + ", ".join(_format_fraction(value) for value in values) + "]"


def _format_term(coefficient: Coeff, power: int, variable: str) -> str:
    if power == 0:
        return _format_fraction(coefficient)

    if power == 1:
        variable_part = variable
    else:
        variable_part = f"{variable}^{power}"

    if coefficient == 1:
        return variable_part
    return f"{_format_fraction(coefficient)}*{variable_part}"


def _format_fraction(value: Coeff) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"
