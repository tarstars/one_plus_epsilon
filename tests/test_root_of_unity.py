from fractions import Fraction
import unittest

from one_plus_epsilon.polynomial import poly
from one_plus_epsilon.root_of_unity import (
    conjugate_inverse_product,
    conjugate_product_trace,
    cyclic_relation_check,
    primitive_inverse_candidate,
    primitive_inverse_check,
)


class RootOfUnityTests(unittest.TestCase):
    def test_direct_inverse_reduces_to_one(self) -> None:
        check = primitive_inverse_check(17)

        self.assertEqual(check.reduced_product, poly([1]))
        self.assertEqual(
            check.inverse,
            primitive_inverse_candidate(17),
        )
        self.assertEqual(check.product_minus_one, tuple(Fraction(-1) for _ in range(17)))

    def test_conjugate_product_finds_one(self) -> None:
        steps = conjugate_product_trace(17)

        self.assertEqual(len(steps), 16)
        self.assertEqual(steps[-1].reduced_product, poly([1]))

    def test_conjugate_inverse_matches_direct_inverse(self) -> None:
        self.assertEqual(
            conjugate_inverse_product(17),
            primitive_inverse_candidate(17),
        )

    def test_cyclic_relation_needs_half_coefficients(self) -> None:
        check = cyclic_relation_check(17)

        self.assertEqual(check.reduced_product, poly([2]))
        self.assertEqual(check.rational_inverse_product, poly([1]))
        self.assertTrue(any(coefficient.denominator == 2 for coefficient in check.rational_inverse))


if __name__ == "__main__":
    unittest.main()
