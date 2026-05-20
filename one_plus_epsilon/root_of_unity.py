"""Polynomial constructions for a primitive odd prime root of unity."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .polynomial import (
    Polynomial,
    add,
    monomial,
    mul,
    one_plus_monomial,
    poly,
    reduce_mod_monic,
    reduce_mod_xn_minus_one,
    scale,
    sub,
)


@dataclass(frozen=True)
class PrimitiveInverseCheck:
    """Data proving ``(1 + eps)^(-1)`` in ``Z[eps]``."""

    degree: int
    cyclotomic: Polynomial
    inverse: Polynomial
    product: Polynomial
    product_minus_one: Polynomial
    reduced_product: Polynomial


@dataclass(frozen=True)
class CyclicRelationCheck:
    """Data for the larger quotient using only ``x^n = 1``."""

    degree: int
    alternating: Polynomial
    product: Polynomial
    reduced_product: Polynomial
    rational_inverse: Polynomial
    rational_inverse_product: Polynomial


@dataclass(frozen=True)
class ProductStep:
    """One reduced multiplication step for conjugate factors."""

    factor_power: int
    factor: Polynomial
    reduced_product: Polynomial


def cyclotomic_prime(p: int) -> Polynomial:
    """Return ``Phi_p(x) = 1 + x + ... + x^(p-1)`` for prime ``p``."""

    require_odd_prime(p)
    return poly([1] * p)


def primitive_inverse_candidate(p: int) -> Polynomial:
    """Return ``-x - x^3 - ... - x^(p-2)`` for odd prime ``p``.

    For ``p = 17`` this is:

        -x - x^3 - x^5 - ... - x^15
    """

    require_odd_prime(p)
    result = poly([0])
    for power in range(1, p - 1, 2):
        result = add(result, monomial(power, -1))
    return result


def primitive_inverse_check(p: int = 17) -> PrimitiveInverseCheck:
    """Build the exact identity proving the primitive-root inverse."""

    modulus = cyclotomic_prime(p)
    inverse = primitive_inverse_candidate(p)
    product = mul(poly([1, 1]), inverse)
    product_minus_one = sub(product, poly([1]))
    reduced_product = reduce_mod_monic(product, modulus)
    return PrimitiveInverseCheck(
        degree=p,
        cyclotomic=modulus,
        inverse=inverse,
        product=product,
        product_minus_one=product_minus_one,
        reduced_product=reduced_product,
    )


def conjugate_product_trace(p: int = 17) -> list[ProductStep]:
    """Multiply ``(1+x), (1+x^2), ..., (1+x^(p-1))`` modulo ``Phi_p``."""

    modulus = cyclotomic_prime(p)
    accumulator = poly([1])
    steps: list[ProductStep] = []
    for power in range(1, p):
        factor = one_plus_monomial(power)
        accumulator = reduce_mod_monic(mul(accumulator, factor), modulus)
        steps.append(
            ProductStep(
                factor_power=power,
                factor=factor,
                reduced_product=accumulator,
            )
        )
    return steps


def conjugate_inverse_product(p: int = 17) -> Polynomial:
    """Return ``product_{k=2}^{p-1} (1+x^k)`` reduced modulo ``Phi_p``."""

    modulus = cyclotomic_prime(p)
    accumulator = poly([1])
    for power in range(2, p):
        accumulator = reduce_mod_monic(
            mul(accumulator, one_plus_monomial(power)),
            modulus,
        )
    return accumulator


def cyclic_relation_check(n: int = 17) -> CyclicRelationCheck:
    """Check what happens in ``Q[x] / (x^n - 1)``.

    For odd ``n``:

        (1+x)(1 - x + x^2 - ... + x^(n-1)) = 1 + x^n

    Reducing by ``x^n = 1`` gives ``2``. Therefore the rational inverse is
    half of the alternating polynomial.
    """

    if n <= 0 or n % 2 == 0:
        raise ValueError("n must be a positive odd integer")
    alternating = poly(Fraction((-1) ** power) for power in range(n))
    product = mul(poly([1, 1]), alternating)
    reduced_product = reduce_mod_xn_minus_one(product, n)
    rational_inverse = scale(alternating, Fraction(1, 2))
    rational_inverse_product = reduce_mod_xn_minus_one(
        mul(poly([1, 1]), rational_inverse),
        n,
    )
    return CyclicRelationCheck(
        degree=n,
        alternating=alternating,
        product=product,
        reduced_product=reduced_product,
        rational_inverse=rational_inverse,
        rational_inverse_product=rational_inverse_product,
    )


def powers_of_one_plus_x(p: int = 17, count: int = 20) -> list[tuple[int, Polynomial]]:
    """Return powers of ``1+x`` reduced modulo ``Phi_p``."""

    if count < 0:
        raise ValueError("count must be non-negative")
    modulus = cyclotomic_prime(p)
    accumulator = poly([1])
    powers: list[tuple[int, Polynomial]] = []
    for exponent in range(1, count + 1):
        accumulator = reduce_mod_monic(mul(accumulator, poly([1, 1])), modulus)
        powers.append((exponent, accumulator))
    return powers


def is_constant(p: Polynomial) -> bool:
    """Return whether a polynomial has degree zero after normalization."""

    return len(p) == 1


def require_odd_prime(p: int) -> None:
    """Validate the prime case where ``Phi_p`` has the simple sum form."""

    if p <= 2 or p % 2 == 0 or not _is_prime(p):
        raise ValueError("degree must be an odd prime; this project defaults to 17")


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    factor = 3
    while factor * factor <= n:
        if n % factor == 0:
            return False
        factor += 2
    return True
