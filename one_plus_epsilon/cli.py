"""Command-line interface for the polynomial checks."""

from __future__ import annotations

import argparse

from .polynomial import coefficient_vector, format_polynomial
from .root_of_unity import (
    conjugate_inverse_product,
    conjugate_product_trace,
    cyclic_relation_check,
    is_constant,
    powers_of_one_plus_x,
    primitive_inverse_check,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Check constructive polynomial identities around a primitive "
            "17th root of unity."
        )
    )
    parser.add_argument(
        "--degree",
        type=int,
        default=17,
        help="odd prime degree to check; default: 17",
    )
    parser.add_argument(
        "--trace-conjugates",
        action="store_true",
        help="print product steps for (1+x), (1+x^2), ..., (1+x^(p-1))",
    )
    parser.add_argument(
        "--powers",
        type=int,
        default=0,
        metavar="N",
        help="print the first N powers of (1+x) modulo Phi_p",
    )
    parser.add_argument(
        "--vectors",
        action="store_true",
        help="also print coefficient vectors in ascending degree order",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    primitive = primitive_inverse_check(args.degree)
    cyclic = cyclic_relation_check(args.degree)
    conjugate_inverse = conjugate_inverse_product(args.degree)

    print(f"Degree: {args.degree}")
    print()
    print("Primitive-root quotient Z[x] / (Phi_p):")
    print(f"  Phi_{args.degree}(x) = {format_polynomial(primitive.cyclotomic)}")
    print(f"  inverse candidate = {format_polynomial(primitive.inverse)}")
    print(f"  (1 + x) * candidate = {format_polynomial(primitive.product)}")
    print(f"  product - 1 = {format_polynomial(primitive.product_minus_one)}")
    print(f"  reduced product = {format_polynomial(primitive.reduced_product)}")
    if args.vectors:
        print(
            "  candidate coefficients = "
            f"{coefficient_vector(primitive.inverse, args.degree - 1)}"
        )
    print()
    print("Conjugate-product construction:")
    print(
        "  product_{k=2}^{p-1} (1 + x^k) reduced = "
        f"{format_polynomial(conjugate_inverse)}"
    )
    print("  This matches the inverse candidate above.")
    print()
    print("Larger cyclic quotient Q[x] / (x^p - 1):")
    print(f"  alternating polynomial = {format_polynomial(cyclic.alternating)}")
    print(f"  (1 + x) * alternating = {format_polynomial(cyclic.product)}")
    print(
        "  reduced by x^p = 1: "
        f"{format_polynomial(cyclic.reduced_product)}"
    )
    print(
        "  rational inverse = "
        f"{format_polynomial(cyclic.rational_inverse)}"
    )
    print(
        "  rational inverse product reduced = "
        f"{format_polynomial(cyclic.rational_inverse_product)}"
    )
    print("  No integer inverse exists here: at x = 1 it would need 2*q(1) = 1.")

    if args.trace_conjugates:
        print()
        print("Trace of conjugate factors modulo Phi_p:")
        for step in conjugate_product_trace(args.degree):
            print(
                f"  after (1 + x^{step.factor_power}): "
                f"{format_polynomial(step.reduced_product)}"
            )

    if args.powers:
        print()
        print("Powers of (1 + x) modulo Phi_p:")
        for exponent, value in powers_of_one_plus_x(args.degree, args.powers):
            marker = " constant" if is_constant(value) else ""
            print(f"  power {exponent:>2}: {format_polynomial(value)}{marker}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
