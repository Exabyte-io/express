import math
import unittest

from express.parsers.apps.nwchem.formats.txt import NwchemTXTParser


def orbital_analysis_block(spin, energies):
    header = f"DFT Final {spin + ' ' if spin else ''}Molecular Orbital Analysis"
    vectors = "\n".join(
        f" Vector {index + 1:4d}  Occ={occupation}  E={energy}" for index, (occupation, energy) in enumerate(energies)
    )
    return f"{header}\n{'-' * len(header)}\n\n{vectors}\n\n center of mass\n"


class NwchemTXTParserTest(unittest.TestCase):
    """
    Covers the selection of orbital analysis sections, which the integration fixtures cannot
    exercise: both of them are closed shell and single channel.
    """

    def setUp(self):
        self.parser = NwchemTXTParser(work_dir=".")

    def test_reads_last_section_of_closed_shell_output(self):
        text = orbital_analysis_block(None, [("2.000000D+00", "-1.0D+00")]) + orbital_analysis_block(
            None, [("2.000000D+00", "-2.0D+00"), ("0.000000D+00", "3.0D-01")]
        )
        self.assertEqual(
            self.parser.eigenvalues_at_vectors(text),
            [
                {"vector": 1, "occupation": 2.0, "energy": -2.0},
                {"vector": 2, "occupation": 0.0, "energy": 0.3},
            ],
        )

    def test_reads_both_channels_of_spin_polarized_output(self):
        text = orbital_analysis_block("Alpha", [("1.000000D+00", "-9.0D+00")]) + orbital_analysis_block(
            "Beta", [("1.000000D+00", "-8.0D+00"), ("0.000000D+00", "5.0D-01")]
        )
        self.assertEqual(
            self.parser.eigenvalues_at_vectors(text),
            [
                {"vector": 1, "occupation": 1.0, "energy": -9.0},
                {"vector": 1, "occupation": 1.0, "energy": -8.0},
                {"vector": 2, "occupation": 0.0, "energy": 0.5},
            ],
        )

    def test_reads_last_step_of_each_channel(self):
        text = "".join(
            [
                orbital_analysis_block("Alpha", [("1.000000D+00", "-9.0D+00")]),
                orbital_analysis_block("Beta", [("1.000000D+00", "-8.0D+00")]),
                orbital_analysis_block("Alpha", [("1.000000D+00", "-7.0D+00")]),
                orbital_analysis_block("Beta", [("1.000000D+00", "-6.0D+00")]),
            ]
        )
        self.assertEqual([orbital["energy"] for orbital in self.parser.eigenvalues_at_vectors(text)], [-7.0, -6.0])

    def test_returns_nothing_without_an_orbital_analysis_section(self):
        self.assertEqual(self.parser.eigenvalues_at_vectors(" Total DFT energy = -76.4\n"), [])


def geometry_block(units, scale, *rows):
    return "\n".join(
        [
            f" Output coordinates in {units} (scale by  {scale} to convert to a.u.)",
            "",
            "  No.       Tag          Charge          X              Y              Z",
            " ---- ---------------- ---------- -------------- -------------- --------------",
            *rows,
            "",
            "      Atomic Mass ",
            "      O                 15.994910",
            "",
        ]
    )


ANGSTROM = ("angstroms", "1.889725989")
ATOMIC_UNITS = ("a.u.", "1.000000000")
ANGSTROM_ROWS = [
    "    1 O                    8.0000     0.00000000     0.00000000     1.00000000",
    "    2 H                    1.0000     0.00000000     0.00000000    -1.00000000",
]


class NwchemTXTParserGeometryTest(unittest.TestCase):
    def setUp(self):
        self.parser = NwchemTXTParser(work_dir=".")

    def coordinates(self, text, index=-1):
        return [[round(v, 6) for v in c["value"]] for c in self.parser.basis(text, index)["coordinates"]]

    def test_selects_the_block_by_index(self):
        text = geometry_block(*ANGSTROM, *ANGSTROM_ROWS) + geometry_block(
            *ANGSTROM,
            "    1 O                    8.0000     0.00000000     0.00000000     0.50000000",
            "    2 H                    1.0000     0.00000000     0.00000000    -0.50000000",
        )
        self.assertEqual([self.coordinates(text, 0)[0][2], self.coordinates(text)[0][2]], [1.0, 0.5])

    def test_bond_length_of_an_atomic_units_block_is_physical(self):
        # test-001's rows verbatim. Read as angstrom they give an O-H of 1.81 A, not 0.9572 A.
        text = geometry_block(
            *ATOMIC_UNITS,
            "    1 O                    8.0000     0.00000000     0.00000000     0.22143053",
            "    2 H                    1.0000     0.00000000     1.43042809    -0.88572213",
            "    3 H                    1.0000     0.00000000    -1.43042809    -0.88572213",
        )
        coordinates = self.coordinates(text)
        self.assertAlmostEqual(math.dist(coordinates[0], coordinates[1]), 0.9572, places=4)
        self.assertAlmostEqual(math.dist(coordinates[0], coordinates[2]), 0.9572, places=4)

    def test_refuses_blocks_that_disagree_on_their_atoms(self):
        # A log truncated mid-table parses as a shorter molecule, which rupy would publish.
        text = geometry_block(*ANGSTROM, *ANGSTROM_ROWS) + geometry_block(*ANGSTROM, ANGSTROM_ROWS[0])
        self.assertIsNone(self.parser.basis(text, -1))

    def test_returns_nothing_without_a_geometry_block(self):
        self.assertIsNone(self.parser.basis(" Total DFT energy = -76.4\n", -1))

    def test_ignores_a_numeric_row_that_happens_to_fit_the_shape(self):
        # A row of bare numbers satisfies the column shape but has no element symbol. It must be
        # skipped, not raise: rupy swallows the exception and final_structure vanishes silently.
        text = geometry_block(*ANGSTROM, *ANGSTROM_ROWS, "    3 1.0000    2.0000    3.0000     4.0000     5.0000")
        self.assertEqual([e["value"] for e in self.parser.basis(text, -1)["elements"]], ["O", "H"])
