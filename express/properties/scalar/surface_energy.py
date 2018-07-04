from express.properties.scalar import ScalarProperty


class SurfaceEnergy(ScalarProperty):

    def __init__(self, name, raw_data, *args, **kwargs):
        super(SurfaceEnergy, self).__init__(name, raw_data, *args, **kwargs)
        self.value = kwargs["value"]
