from unittest.mock import MagicMock
from tests.unit import UnitTestBase
from express.properties.non_scalar.two_dimensional_plot.wavefunction_amplitude import WavefunctionAmplitude


class WavefunctionAmplitudeTest(UnitTestBase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_wavefunction_amplitude_with_data(self):
        x_data = [0.0, 0.0050251256, 0.0100502513, 0.0150753769, 0.0201005025]
        y_data = [0.0000322091, 0.0000072134, -0.0000218274, -0.0000540398, -0.0000883573]
        
        parser = MagicMock()
        parser.wavefunction_amplitude.return_value = [x_data, y_data]
        
        # Create property
        property_ = WavefunctionAmplitude("wavefunction_amplitude", parser)
        result = property_.serialize_and_validate()
        
        # Verify structure
        self.assertEqual(result['name'], 'wavefunction_amplitude')
        self.assertIn('xDataArray', result)
        self.assertIn('yDataSeries', result)
        self.assertIn('xAxis', result)
        self.assertIn('yAxis', result)
        
        # Verify axis labels and units
        self.assertEqual(result['xAxis']['label'], 'coordinate')
        self.assertEqual(result['xAxis']['units'], 'angstrom')
        self.assertEqual(result['yAxis']['label'], 'amplitude')
        self.assertEqual(result['yAxis']['units'], 'a.u.')
        
        # Verify data
        self.assertEqual(result['xDataArray'], x_data)
        self.assertEqual(len(result['yDataSeries']), 1)
        self.assertEqual(result['yDataSeries'][0], y_data)

