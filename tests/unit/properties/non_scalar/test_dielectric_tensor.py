from unittest.mock import MagicMock
import numpy as np
from typing import List

from express.properties.non_scalar.dielectric_tensor import DielectricTensor
from tests.unit import UnitTestBase

MOCK_DATA = [
    [0.000000000, 20.137876673, 20.137876704, 20.137849785],
    [0.060120240, 20.143821034, 20.143821066, 20.143794147],
    [0.120240481, 20.161680126, 20.161680158, 20.161653237],
    [0.180360721, 20.191532277, 20.191532311, 20.191505388],
]


class DielectricTensorTest(UnitTestBase):
    def setUp(self):
        super().setUp()
        self.mock_parsed_tensor = {
            "depsi_prefix.dat": self.mock_loadtxt(MOCK_DATA),
            "depsr_prefix.dat": self.mock_loadtxt(MOCK_DATA),
            "uepsi_prefix.dat": self.mock_loadtxt(MOCK_DATA),
            "uepsr_prefix.dat": self.mock_loadtxt(MOCK_DATA),
        }

    def tearDown(self):
        super().tearDown()

    def mock_loadtxt(self, data: List[List[float]]):
        dtype = np.dtype([("energy", float), ("eps", (float, 3))])
        return np.array([(row[0], tuple(row[1:])) for row in data], dtype=dtype)

    def test_dielectric_tensor(self):
        parser = MagicMock()
        parser.attach_mock(MagicMock(return_value=self.mock_parsed_tensor), "dielectric_tensor")
        property_ = DielectricTensor("dielectric_tensor", parser)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), DIELECTRIC_TENSOR)

DIELECTRIC_TENSOR = {
    "name": "dielectric_tensor",
    "values": [
        {
            "part": "real",
            "spin": 0.5,
            "frequencies": [
                0.000000000,
                0.060120240,
                0.120240481,
                0.180360721
            ],
            "components": [
                [20.137876673, 20.137876704, 20.137849785],
                [20.143821034, 20.143821066, 20.143794147],
                [20.161680126, 20.161680158, 20.161653237],
                [20.191532277, 20.191532311, 20.191505388],
            ]
        },
        {
            "part": "imaginary",
            "spin": 0.5,
            "frequencies": [
                0.000000000,
                0.060120240,
                0.120240481,
                0.180360721
            ],
            "components": [
                [20.137876673, 20.137876704, 20.137849785],
                [20.143821034, 20.143821066, 20.143794147],
                [20.161680126, 20.161680158, 20.161653237],
                [20.191532277, 20.191532311, 20.191505388],
            ]
        },
        {
            "part": "real",
            "spin": -0.5,
            "frequencies": [
                0.000000000,
                0.060120240,
                0.120240481,
                0.180360721
            ],
            "components": [
                [20.137876673, 20.137876704, 20.137849785],
                [20.143821034, 20.143821066, 20.143794147],
                [20.161680126, 20.161680158, 20.161653237],
                [20.191532277, 20.191532311, 20.191505388],
            ]
        },
        {
            "part": "imaginary",
            "spin": -0.5,
            "frequencies": [
                0.000000000,
                0.060120240,
                0.120240481,
                0.180360721
            ],
            "components": [
                [20.137876673, 20.137876704, 20.137849785],
                [20.143821034, 20.143821066, 20.143794147],
                [20.161680126, 20.161680158, 20.161653237],
                [20.191532277, 20.191532311, 20.191505388],
            ]
        }
    ]
}
