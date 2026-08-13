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


def geometry_block(units, scale, rows):
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


class NwchemTXTParserGeometryTest(unittest.TestCase):
    """
    Covers what the integration fixtures cannot: that the units the block declares are honoured,
    and that a run with no geometry block at all returns None rather than raising.
    """

    ANGSTROM_ROWS = [
        "    1 O                    8.0000     0.00000000     0.00000000     1.00000000",
        "    2 H                    1.0000     0.00000000     0.00000000    -1.00000000",
    ]

    def setUp(self):
        self.parser = NwchemTXTParser(work_dir=".")

    def test_reads_first_and_last_block_of_an_optimization(self):
        text = geometry_block("angstroms", "1.889725989", self.ANGSTROM_ROWS) + geometry_block(
            "angstroms",
            "1.889725989",
            [
                "    1 O                    8.0000     0.00000000     0.00000000     0.50000000",
                "    2 H                    1.0000     0.00000000     0.00000000    -0.50000000",
            ],
        )
        initial = self.parser.initial_basis(text)["coordinates"]
        final = self.parser.final_basis(text)["coordinates"]
        self.assertAlmostEqual(initial[0]["value"][2] - initial[1]["value"][2], 2.0)
        self.assertAlmostEqual(final[0]["value"][2] - final[1]["value"][2], 1.0)

    def test_converts_a_block_printed_in_atomic_units(self):
        text = geometry_block(
            "a.u.",
            "1.000000000",
            [
                "    1 O                    8.0000     0.00000000     0.00000000     1.88972599",
                "    2 H                    1.0000     0.00000000     0.00000000    -1.88972599",
            ],
        )
        coordinates = self.parser.final_basis(text)["coordinates"]
        self.assertAlmostEqual(coordinates[0]["value"][2] - coordinates[1]["value"][2], 2.0, places=6)

    def test_centers_the_basis_inside_the_derived_cell(self):
        text = geometry_block("angstroms", "1.889725989", self.ANGSTROM_ROWS)
        edge = self.parser.final_lattice_vectors(text)["vectors"]["a"][0]
        for coordinate in self.parser.final_basis(text)["coordinates"]:
            for value in coordinate["value"]:
                self.assertGreaterEqual(value, 0.0)
                self.assertLessEqual(value, edge)

    def test_returns_nothing_without_a_geometry_block(self):
        self.assertIsNone(self.parser.final_basis(" Total DFT energy = -76.4\n"))
        self.assertIsNone(self.parser.final_lattice_vectors(" Total DFT energy = -76.4\n"))

    def test_ignores_a_numeric_row_that_happens_to_fit_the_shape(self):
        # A row of bare numbers satisfies the column shape but has no element symbol. It must be
        # skipped, not raise: rupy swallows the exception and final_structure vanishes silently.
        text = geometry_block(
            "angstroms",
            "1.889725989",
            self.ANGSTROM_ROWS + ["    3 1.0000    2.0000    3.0000     4.0000     5.0000"],
        )
        basis = self.parser.final_basis(text)
        self.assertEqual([e["value"] for e in basis["elements"]], ["O", "H"])
