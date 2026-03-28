from express.properties.scalar import ScalarProperty


class ThermalCorrectionToEnthalpy(ScalarProperty):
    """
    Thermal correction to enthalpy property class.
    """

    def __init__(self, name, parser, *args, **kwargs):
        super(ThermalCorrectionToEnthalpy, self).__init__(name, parser, *args, **kwargs)
        self.value = self.parser.thermal_correction_to_enthalpy()
