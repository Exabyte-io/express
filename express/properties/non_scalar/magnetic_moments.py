from express.properties.utils import to_array_with_ids
from express.properties.non_scalar import NonScalarProperty


class MagneticMoments(NonScalarProperty):

    def __init__(self, name, parser, *args, **kwargs):
        super(MagneticMoments, self).__init__(name, parser, *args, **kwargs)

    def _serialize(self):
        return {
            'name': self.name,
            "units": self.manifest["defaults"]["units"],
            "values": to_array_with_ids(self.parser.magnetic_moments())
        }
