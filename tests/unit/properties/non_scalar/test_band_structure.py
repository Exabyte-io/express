from tests.unit import UnitTestBase
from tests.data.raw_data import BAND_RAW_DATA
from express.properties.non_scalar.two_dimensional_plot.band_structure import BandStructure

BAND_STRUCTURE = {
    "xAxis": {
        "units": "crystal",
        "label": "kpoints"
    },
    "yDataSeries": [
        [
            -5.5990059,
            -3.30219959,
            -3.30220019,
            -1.51073812,
            -3.30221054,
            -1.51074222
        ],
        [
            6.26931638,
            -0.66503974,
            -0.6650363,
            -1.51072293,
            -0.66501391,
            -1.5107195
        ],
        [
            6.26931998,
            5.06084876,
            5.06084821,
            3.41069883,
            5.06085301,
            3.41069761
        ],
        [
            6.26934533,
            5.0608702,
            5.06086954,
            3.41070722,
            5.06085524,
            3.41071003
        ],
        [
            8.71135349,
            7.69496909,
            7.69496137,
            6.91957625,
            7.69495606,
            6.91957636
        ],
        [
            8.71135587,
            9.49274379,
            9.49273868,
            6.91958498,
            9.49273487,
            6.91958424
        ],
        [
            8.71135838,
            9.49275618,
            9.49275401,
            16.14829919,
            9.49273798,
            16.14830113
        ],
        [
            9.41550185,
            13.89571002,
            13.89571914,
            16.1483028,
            13.89571883,
            16.14830247
        ]
    ],
    "name": "band_structure",
    "yAxis": {
        "units": "eV",
        "label": "energy"
    },
    "spin": [
        0.5,
        0.5,
        0.5,
        0.5,
        0.5,
        0.5,
        0.5,
        0.5
    ],
    "xDataArray": [
        [
            0.0,
            0.0,
            0.0
        ],
        [
            -4.8471013318887174e-17,
            -4.8471013318887174e-17,
            -0.5000000000000001
        ],
        [
            0.0,
            -0.4999999999999998,
            0.0
        ],
        [
            -4.8471013318887174e-17,
            -0.4999999999999998,
            -0.5000000000000001
        ],
        [
            -0.4999999999999998,
            6.584042720160102e-17,
            0.0
        ],
        [
            -0.4999999999999998,
            -0.4999999999999998,
            0.0
        ]
    ]
}


class BandStructureTest(UnitTestBase):
    def setUp(self):
        super(BandStructureTest, self).setUp()

    def tearDown(self):
        super(BandStructureTest, self).setUp()

    def test_band_structure(self):
        property_ = BandStructure("band_structure", raw_data=BAND_RAW_DATA)
        self.assertDeepAlmostEqual(property_.serialize_and_validate(), BAND_STRUCTURE)
