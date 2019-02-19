from express.properties.scalar import ScalarProperty


class SurfaceEnergy(ScalarProperty):

    def __init__(self, name, parser, *args, **kwargs):
        super(SurfaceEnergy, self).__init__(name, parser, *args, **kwargs)
        self.value = kwargs["value"]
