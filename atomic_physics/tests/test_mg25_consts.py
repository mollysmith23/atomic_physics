"""
References:
[1] - R. Srinivas, Laser-free trapped-ion quantum logic with a radiofrequency
        magnetic field gradient, PhD Thesis, University of Colorado (2016)
"""

import unittest
from atomic_physics.ions import mg25
from atomic_physics.utils import field_insensitive_point
import numpy as np

S12_31_21_clock_field = 212.8e-4  # [1]
MW_transition_freqs = {
    (3, 2): 1.326456e9,
    (2, 2): 1.460516e9,
    (1, 2): 1.573543e9,
    (2, 1): 1.573432e9,
    (1, 1): 1.686459e9,
    (0, 1): 1.786044e9,
    (0, -1): 1.975445e9,
}  # [1]


class TestMg25Consts(unittest.TestCase):
    def test_s12_clock(self):
        """Look for field-insensitive S1/2 3,1 -> S1/2 2,1 transition at 212.8 G"""
        ion = mg25.Mg25(level_filter=[mg25.S12])

        ion.setB(S12_31_21_clock_field)
        l_index = ion.index(mg25.S12, 1, F=3)
        u_index = ion.index(mg25.S12, 1, F=2)

        # 212.8 G
        model_field_independent_point = field_insensitive_point(
            ion, l_index, u_index, B0=S12_31_21_clock_field
        )
        self.assertAlmostEqual(
            model_field_independent_point, S12_31_21_clock_field, places=5
        )

    def test_mw_transitions(self):
        """
        Check microwave transition frequencies in the ground state manifold
        """
        ion = mg25.Mg25(level_filter=[mg25.S12])

        ion.setB(S12_31_21_clock_field)
        l_index = ion.index(mg25.S12, 1, F=3)
        u_index = ion.index(mg25.S12, 1, F=2)

        model_field_independent_point = field_insensitive_point(
            ion, l_index, u_index, B0=S12_31_21_clock_field
        )
        ion.setB(model_field_independent_point)

        for key, value in MW_transition_freqs.items():
            freq_model = (
                ion.delta(
                    ion.index(mg25.S12, F=3, M=key[0]),
                    ion.index(mg25.S12, F=2, M=key[1]),
                )
                / 2
                * np.pi
            )

            self.assertAlmostEqual(freq_model, value, places=4)