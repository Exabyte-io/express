from express.properties.scalar import ScalarProperty


class ThermalCorrectionToEnergy(ScalarProperty):
    """
    Thermal correction to energy property class.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(ThermalCorrectionToEnergy, self).__init__(name, parser, *args, **kwargs)
        self.value = self.parser.thermal_correction_to_energy()
