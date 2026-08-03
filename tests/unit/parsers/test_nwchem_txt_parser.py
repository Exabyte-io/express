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
